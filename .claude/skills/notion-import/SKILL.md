---
name: notion-import
description: This skill should be used when the user explicitly asks to import, consolidate, or migrate their existing Notion notes/pages into the Obsidian knowledge base (e.g. "import my Notion notes", "consolidate my Notion 'AI Using' tree into the vault", "bring my Notion pages in"). It orchestrates a one-time bulk migration via the connected Notion MCP: discover the page tree, normalize blocks to markdown, stage, dedup and map each page to the vault's four-actions judgment, batch-review with the user, then apply each as a normal atomic operation. Do NOT use for discussing Notion content, for single-note capture (use the normal Scribe flow), or for non-Notion sources.
---

# Notion Import

## Overview

Migrate an existing Notion corpus into the Obsidian vault as atomic, wikilinked notes. This is a
**bulk one-time onboarding migration**, not the per-capture Scribe flow. It is a thin
orchestration: it sequences discovery → normalize → stage → reconcile → apply, but defers every
*judgment* (new note vs append, duplicates, linking, templates) to the vault's existing rules. It
never restates them.

The only thing bulk changes versus single capture is **confirmation granularity**: review is
batched (you cannot confirm hundreds of pages one at a time). Everything else — including the
write protocol — stays identical to a normal capture.

## When to use

Trigger only when BOTH hold:

- The source is **Notion**, reached via the **connected Notion MCP**.
- The user expressed **explicit migration intent** — Manage mode per `CLAUDE.md` requires it.

Do **not** trigger for: discussing/reading Notion content (Discuss mode), single-note capture
(normal Scribe flow), or any non-Notion source.

## Language fidelity — do not translate (Notion-import-specific)

Imported content stays in its **source language**: whatever language a Notion page used, the
resulting note keeps it — titles and body alike (English stays English, Chinese stays Chinese).
**Never translate during import** — translation risks corrupting the original meaning. Translate
only on an explicit, per-request user instruction.

This rule is scoped to *stored Notion content*. It does **not** change the agent's normal behavior:
conversation and all other captures still follow the user's configured language preference
(`~/.claude/CLAUDE.md`). Two different axes — content fidelity vs. conversational language.

Because relationships are judged by **meaning, not surface text**, wikilinks may legitimately cross
languages — an English note and a Chinese note on the same topic should link. Language is never a
dedup key (see step 4). When a cross-language pairing is uncertain, ask via a question card (step 5).

## Authority — defer to the rules, never restate them

Canonical judgment lives in the repo rules. Read and apply them in place; do not duplicate them.

- `CLAUDE.md` — Scribe modes, vault principles, confirmation gates.
- `.claude/rules/four-actions.md` — Assimilation/Creation 5-dimension judgment; "one capture ≠ one action".
- `.claude/rules/substance-test.md` — concept-level threshold for a new note.
- `.claude/rules/single-source-of-truth.md` — duplicate/conflict detection and handling.
- `.claude/rules/templates.md` — template selection.
- `.claude/rules/linking.md` — wikilink decisions.
- `.claude/rules/atomic-operation.md` + `.claude/rules/log-schema.md` — 3-step write, JSONL log, one commit per action.

**No rule deviation.** Each applied page is a full atomic operation (one edit + one JSONL line +
one commit). Bulk only batches the *user review*, not the write. Per-note confirmation is replaced
by one batched approval that still surfaces every title / location / template per `CLAUDE.md`.

## Prerequisites

1. Confirm the Notion MCP is reachable — call `API-get-self`. If it fails, stop and tell the user
   to connect the integration.
2. Remember the integration only sees pages **explicitly shared with it**. If the user expects more
   than what `API-post-search` returns, have them share the parent page(s) in Notion
   (page → ••• → Connections) before proceeding.
3. This flow assumes a **near-empty vault** (first-run onboarding). If the vault already holds
   substantial notes, say so — dedup load against existing notes grows, and the user may want a
   smaller scope.

## Workflow

### 1. Discover the tree and confirm scope

- List accessible pages with `API-post-search` (empty `query` returns all shared pages).
- Reconstruct the hierarchy from each page's `parent` field. Note that nested pages also appear as
  `child_page` blocks inside a parent's content (surfaced in step 2).
- Default scope is **all accessible pages**. Present the full tree, confirm the user wants
  everything (or let them narrow it), and get explicit go-ahead before any fetch.

### 2. Fetch and normalize each page

For each in-scope page:

- Read its content with `API-get-block-children` (paginate via `start_cursor`; recurse into
  blocks that have `has_children: true`).
- Convert blocks to clean Obsidian markdown using `references/notion-block-mapping.md`.
- Treat each `child_page` block as a **separate page** → its own note, queued for the same flow.
- Preserve the user's words **verbatim and in the source language** (titles + body); do not
  summarize, rewrite, or translate — this is migration, not authoring (see "Language fidelity").
- If normalization is lossy or ambiguous for a block (unreadable, possible content loss, unclear
  structure), flag that page for a content-accuracy question card at review (step 5) — never invent.
- Record provenance for the log only: Notion page id, `url`, title, created/last-edited times.
  Provenance goes in the JSONL `reason`/`targets`, **not** in note bodies (no proactive frontmatter).

### 3. Stage (no vault writes yet)

- Write each normalized note to a gitignored staging dir (`.import-staging/`).
- Build a **manifest**: for every page → proposed note title, source id/url, parent (for linking),
  and a placeholder for the action verdict (filled in step 4).
- Finalize note titles here so wikilinks resolve correctly at apply time.

### 4. Reconcile — map each page to a four-actions verdict

For **each** staged page independently:

- Run the 5-dimension judgment (`four-actions.md`) against vault-search candidates → Creation,
  Assimilation, SSOT-raise, or defer. Apply the concept-level Substance Test (`substance-test.md`)
  before any Creation.
- Dedup **within the import set** too: if two Notion pages describe the same concept, do not create
  two notes — raise per `single-source-of-truth.md`. Compare by **meaning, not surface text**, so
  cross-language overlaps are caught; language is never a dedup key.
- Map the Notion hierarchy to **wikilinks**, not folders (vault principle: no proactive structure).
  A child page links to its parent; a container page with no real content may not pass the Substance
  Test → defer or fold into a hub link, per the rules.
- Convert Notion page-mentions / inter-page links to `[[wikilinks]]` (see the mapping reference).
- **Cross-language linking**: link same/similar-topic notes even when they are in different
  languages (meaning-based, per `linking.md`). When uncertain whether two cross-language notes are
  the *same concept* (a potential SSOT merge) or *merely related* (a wikilink), do not guess —
  escalate via a question card (step 5).
- Select a template per `templates.md`.
- Write each verdict (action + per-dimension reasoning + substance-test drafts) into the manifest.

### 5. Batch review with the user

- Present the manifest as a single review: each page, its proposed action (Create / Assimilate /
  SSOT-raise / defer), target note, template, and links.
- The user approves, edits, or rejects per row, or in groups. This batched approval satisfies the
  `CLAUDE.md` confirm-before-create gate for the whole set.
- **Uncertain → question card.** For any genuinely ambiguous decision — uncertain links (especially
  cross-language), possible duplicates, or doubtful content accuracy — surface it as an
  `AskUserQuestion` question card rather than guessing. Resolve these before applying.
- Do not apply anything until approved.

### 6. Apply — one atomic operation per page

For each approved page, in dependency order (parents before children so links resolve):

- Execute its action: create/append the note, write wikilinks per the manifest.
- Append one JSONL line per `log-schema.md` with the per-dimension reasoning + provenance.
- Commit that single action per `atomic-operation.md` (`[executed] <action>: <targets> | <reason>`).
- On any duplicate/conflict surfaced late, stop and raise per `single-source-of-truth.md` — never
  silently merge.

### 7. Cleanup

- After all approved actions are applied and committed, delete the `.import-staging/` dir.
- Report a summary: counts of created / assimilated / deferred / raised, and any pages skipped.

## Constraints

- **Agent ≠ author** — normalized content preserves the user's words; draft defining sentences are
  probes, not final wording.
- **Relationships are wikilinks only** — never inline-copy content between notes
  (`single-source-of-truth.md`, `linking.md`).
- **No proactive structure** — no folders/tags/properties to mirror Notion's tree; hierarchy is
  expressed via wikilinks.
- **Batched-confirmation, still gated** — no vault write before the batch approval in step 5.
- **Atomic per page** — never collapse multiple pages into one commit; the write protocol is
  unchanged from single capture.
- **Source-language fidelity** — never translate imported content; preserve each note's original
  language (titles + body). Translate only on explicit user request. Conversation and other captures
  still follow the user's own language preference.
- **Link by meaning, across languages** — wikilinks may connect same/similar-topic notes regardless
  of language; language is never a dedup key.
- **Uncertain → ask, don't guess** — resolve ambiguous links or content-accuracy doubts via question
  cards before any write.
