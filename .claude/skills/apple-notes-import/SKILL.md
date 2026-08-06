---
name: apple-notes-import
description: This skill should be used when the user explicitly asks to import, consolidate, or migrate their existing Apple Notes into the Obsidian knowledge base (e.g. "import my Apple Notes", "bring my iPhone/Mac notes into the vault", "migrate my Notes app into Obsidian"). It orchestrates a one-time bulk migration via local AppleScript (osascript) on this Mac — there is no Apple cloud API: discover the accounts/folders tree, dump each note's HTML body + metadata, normalize to markdown with pandoc, stage, dedup and map each note to the vault's four-actions judgment, batch-review with the user, then apply each as a normal atomic operation. Do NOT use for discussing Apple Notes content, for single-note capture (use the normal Scribe flow), or for non-Apple sources (Notion has its own skill).
---

# Apple Notes Import

## Overview

Migrate an existing Apple Notes corpus into the Obsidian vault as atomic, wikilinked notes. This is
a **bulk one-time onboarding migration**, not the per-capture Scribe flow. It is a thin
orchestration: it sequences discover → dump → normalize → stage → reconcile → apply, but defers
every *judgment* (new note vs append, duplicates, linking, templates) to the vault's existing rules.
It never restates them.

It is the **sibling of `notion-import`** and shares that skill's entire pipeline. Only two pieces
are Apple-specific:

- **Connector** — local **AppleScript** (`osascript`), because Apple Notes has **no public cloud
  API** (unlike Notion's API/MCP). Access is to the Notes app on *this* Mac.
- **Normalizer** — Apple's **HTML** note body → markdown via **pandoc**, then a small Apple-specific
  cleanup pass (`references/apple-notes-html-mapping.md`), instead of Notion-blocks → markdown.

Everything else — staging, four-actions judgment, SSOT dedup, batched review, the atomic write
protocol — is identical to a normal capture.

## When to use

Trigger only when BOTH hold:

- The source is **Apple Notes**, reached via **local AppleScript on this Mac**.
- The user expressed **explicit migration intent** — Manage mode per `CLAUDE.md` requires it.

Do **not** trigger for: discussing/reading Apple Notes content (Discuss mode), single-note capture
(normal Scribe flow), or any non-Apple source (Notion → `notion-import`).

## Language fidelity — do not translate

Imported content stays in its **source language** — titles and body alike (Chinese stays Chinese,
English stays English). **Never translate during import**; translation risks corrupting the original
meaning. Translate only on an explicit, per-request user instruction.

This rule is scoped to *stored note content*. It does **not** change the agent's normal behavior:
conversation and all other captures still follow the user's configured language preference
(`~/.claude/CLAUDE.md`). Two different axes — content fidelity vs. conversational language.

Because relationships are judged by **meaning, not surface text**, wikilinks may legitimately cross
languages — an English note and a Chinese note on the same topic should link. Language is never a
dedup key. When a cross-language pairing is uncertain, ask via a question card (step 5).

## Authority — defer to the rules, never restate them

Canonical judgment lives in the repo rules. Read and apply them in place; do not duplicate them.

- `CLAUDE.md` — Scribe modes, vault principles, confirmation gates.
- `.claude/rules/four-actions.md` — Assimilation/Creation 5-dimension judgment; "one capture ≠ one action".
- `.claude/rules/substance-test.md` — concept-level threshold for a new note.
- `.claude/rules/single-source-of-truth.md` — duplicate/conflict detection and handling.
- `.claude/rules/templates.md` — template selection.
- `.claude/rules/linking.md` — wikilink decisions.
- `.claude/rules/atomic-operation.md` + `.claude/rules/log-schema.md` — 3-step write, JSONL log, one commit per action.

**No rule deviation.** Each applied note is a full atomic operation (one edit + one JSONL line +
one commit). Bulk only batches the *user review*, not the write. Per-note confirmation is replaced
by one batched approval that still surfaces every title / location / template per `CLAUDE.md`.

## Prerequisites

1. **Platform** — this skill only works on **macOS** with the **Notes app** signed in. It reads the
   local Notes database through AppleScript; there is no remote/cloud path.
2. **Automation permission (TCC)** — the first `osascript` call that controls Notes triggers a macOS
   prompt ("<your terminal> wants to control Notes"). The user must **Allow** it (or enable it under
   System Settings → Privacy & Security → Automation → <terminal> → Notes). Until granted, calls
   error with `-1743`. This is a one-time grant per controlling app. It is **not** an Apple-account
   login — there is no OAuth for Notes.
3. **pandoc** — required for normalization. Verify with `command -v pandoc`; if missing, tell the
   user to `brew install pandoc` before proceeding.
4. **Locked notes** — password-protected notes are invisible to AppleScript: their body cannot be
   read. They are dumped with `locked true` and an empty body, and must be **reported as skipped**
   at review — never silently dropped.
5. **Scale** — this flow assumes a **near-empty vault** (first-run onboarding). If the vault already
   holds substantial notes, say so — dedup load against existing notes grows. AppleScript bulk body
   access is also slow at hundreds of notes; warn if the corpus is large.

## Workflow

Let `STAGE="$(pwd)/.import-staging/apple-notes"` (gitignored). Scripts live in
`.claude/skills/apple-notes-import/scripts/`.

### 1. Discover the tree and confirm scope

List accounts, folders, and note counts (cheap — no bodies) and present the tree:

```bash
osascript -e 'tell application "Notes"
set out to ""
repeat with a in accounts
  set out to out & (name of a) & linefeed
  repeat with f in folders of a
    set out to out & "  " & (name of f) & " (" & (count of notes of f) & ")" & linefeed
  end repeat
end repeat
return out
end tell'
```

Default scope is **all accounts/folders**. Present the tree, confirm the user wants everything (or
let them narrow to specific accounts/folders), and get explicit go-ahead before any dump.

### 2. Dump and normalize

Run the connector, then the normalizer:

```bash
osascript .claude/skills/apple-notes-import/scripts/dump_notes.applescript "$STAGE"
.claude/skills/apple-notes-import/scripts/normalize.sh "$STAGE"
```

This writes, per note: `raw/<index>.html` (verbatim body), `meta/<index>.meta` (tab-separated:
id, account, folder, title, created, modified, attachments, locked), and `md/<index>.md` (pandoc
draft). Then, on each `md/<index>.md`, apply the Apple-specific cleanup in
`references/apple-notes-html-mapping.md` (drop duplicated title heading, strip `<br>` backslashes,
remove empty-heading garbage, collapse blank lines). Preserve the user's words **verbatim and in the
source language** — this is migration, not authoring.

If normalization is lossy or ambiguous for a note (malformed table, dead internal link, unreadable
content), flag that note for a content-accuracy question card at review (step 5) — never invent.
Record provenance (Apple note id, account/folder, created/modified) for the **log only**; it goes in
the JSONL `reason`/`targets`, not in note bodies (no proactive frontmatter).

### 3. Stage (no vault writes yet)

- The normalized notes already live in `STAGE` (gitignored) — that is the staging area.
- Build a **manifest**: for every note → proposed note title (from `meta` title, or the note's first
  heading), source id, account/folder (for linking hints), attachment count, and a placeholder for
  the action verdict (filled in step 4).
- Finalize note titles here so wikilinks resolve correctly at apply time.

### 4. Reconcile — map each note to a four-actions verdict

For **each** staged note independently:

- Run the 5-dimension judgment (`four-actions.md`) against vault-search candidates → Creation,
  Assimilation, SSOT-raise, or defer. Apply the concept-level Substance Test (`substance-test.md`)
  before any Creation.
- Dedup **within the import set** too: if two notes describe the same concept, do not create two
  notes — raise per `single-source-of-truth.md`. Compare by **meaning, not surface text**, so
  cross-language overlaps are caught; language is never a dedup key.
- Map the Apple folder hierarchy to **wikilinks**, not folders (vault principle: no proactive
  structure). A note may link to a sibling/parent topic; an empty container folder is not a note.
- Convert surviving inter-note links to `[[wikilinks]]` where the target is also imported
  (see the mapping reference); drop dead internal links, keep the text.
- Select a template per `templates.md`.
- Write each verdict (action + per-dimension reasoning + substance-test drafts) into the manifest.

### 5. Batch review with the user

- Present the manifest as a single review: each note, its proposed action (Create / Assimilate /
  SSOT-raise / defer), target note, template, and links.
- Report **skipped locked notes** and **notes with attachments** (best-effort: surface the count so
  the user decides whether to export attachments into `Sources/` and embed via `![[...]]`,
  or skip).
- The user approves, edits, or rejects per row, or in groups. This batched approval satisfies the
  `CLAUDE.md` confirm-before-create gate for the whole set.
- **Uncertain → question card.** For any genuinely ambiguous decision — uncertain links (especially
  cross-language), possible duplicates, doubtful content accuracy — surface it as an
  `AskUserQuestion` card rather than guessing. Resolve these before applying.
- Do not apply anything until approved.

### 6. Apply — one atomic operation per note

For each approved note, in dependency order (parents/targets before children so links resolve):

- Execute its action: create/append the note, write wikilinks per the manifest.
- Append one JSONL line per `log-schema.md` with the per-dimension reasoning + provenance
  (Apple note id, account/folder, created/modified).
- Commit that single action per `atomic-operation.md` (`[executed] <action>: <targets> | <reason>`).
- On any duplicate/conflict surfaced late, stop and raise per `single-source-of-truth.md` — never
  silently merge.

### 7. Cleanup

- After all approved actions are applied and committed, delete the `STAGE` dir.
- Report a summary: counts of created / assimilated / deferred / raised, notes skipped (locked),
  and notes flagged for attachments.

## Constraints

- **Local-only, no cloud** — Apple Notes has no public API; this reads the Notes app on this Mac via
  AppleScript. Off this machine, or without Automation permission, the skill cannot run.
- **Agent ≠ author** — normalized content preserves the user's words; cleanup is format-only; draft
  defining sentences are probes, not final wording.
- **Relationships are wikilinks only** — never inline-copy content between notes
  (`single-source-of-truth.md`, `linking.md`).
- **No proactive structure** — no folders/tags/properties to mirror the Notes tree; hierarchy is
  expressed via wikilinks.
- **Batched-confirmation, still gated** — no vault write before the batch approval in step 5.
- **Atomic per note** — never collapse multiple notes into one commit; the write protocol is
  unchanged from single capture.
- **Source-language fidelity** — never translate imported content; preserve each note's original
  language (titles + body). Translate only on explicit user request.
- **Link by meaning, across languages** — wikilinks may connect same/similar-topic notes regardless
  of language; language is never a dedup key.
- **Locked notes skipped, attachments best-effort** — never silently drop either; surface both at
  review.
- **Uncertain → ask, don't guess** — resolve ambiguous links or content-accuracy doubts via question
  cards before any write.
