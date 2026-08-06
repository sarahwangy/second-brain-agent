# Apple Notes HTML → markdown — cleanup reference

`scripts/normalize.sh` runs pandoc (`html → gfm-raw_html`) to produce a **draft** markdown per
note. pandoc handles the bulk (headings, lists, nesting, bold/italic, links, tables). This file
lists the **Apple-Notes-specific artifacts** the agent must clean on the staged draft before the
four-actions judgment — they recur because of how the Notes app emits its HTML `body`.

The agent applies these as mechanical format fixes. They are **not** authoring — the user's words are
preserved verbatim (Agent ≠ author; see `substance-test.md`). When a fix is ambiguous (could change
meaning), leave it and flag the note for a content-accuracy question card at review.

## Observed artifacts (fix every time)

### 1. Leading title heading — DROP it
Apple stores the note's first line as an `<h1>` at the top of the body, duplicating the note's
`name` (which becomes the Obsidian filename). Keeping it = the title appears twice.

- **Rule:** if the draft's first heading text equals the note's `title` (from the `.meta` file),
  delete that heading line. If they differ, keep it (it's a real in-body heading).

```
draft:                       cleaned:
# 健身计划            →       (removed — equals note title)
- 需要做的五项：             - 需要做的五项：
```

### 2. Trailing `\` hard-break markers — STRIP
Apple puts `<br>` at the end of nearly every `<li>`/line. pandoc renders these as a line-ending
backslash (`gfm` hard break). Inside notes they are formatting noise, not intentional breaks.

- **Rule:** remove a trailing `\` at end of a line (and the hard break it encodes). Keep the line's
  text and its list indentation.

```
draft:                       cleaned:
- 引体向上\           →       - 引体向上
- 俯卧撑\                     - 俯卧撑
```

### 3. Empty-heading garbage — REMOVE
An empty Apple heading `<h1><br></h1>` (common as a blank second line) becomes a stray `\` line
followed by a setext underline (`=` for h1, `-` for h2).

- **Rule:** delete lone `\` lines and any line consisting only of `=` or `-` underline characters
  that has no heading text above it.

```
draft:                       cleaned:
# 健身计划                   (title removed per rule 1)
                     →
\                            (both lines removed)
=
```

### 4. Excess blank lines — COLLAPSE
After removing artifacts, collapse runs of 2+ blank lines into a single blank line.

## Handled by pandoc (verify, usually fine)

- **Nested lists** — preserved with 2-space indentation (Obsidian-compatible). Keep as-is.
- **Bold / italic** — `<b>`/`<i>` → `**`/`*`. Fine.
- **Links** — `<a href="...">text</a>` → `[text](url)`. Keep external URLs as markdown links.
  Internal Notes links (`note://`, `applenotes:`) rarely survive meaningfully → if one appears and
  the target note is also being imported, consider a `[[wikilink]]` (per `linking.md`); otherwise
  drop the dead link and keep the text. When unsure, flag for review.
- **Tables** — `<table>` → GFM pipe table. Verify alignment didn't collapse; flag if malformed.

## No clean markdown equivalent (decide per case)

- **Underline** (`<u>`) — markdown has none. Drop the underline, keep the text (default), unless the
  user's emphasis would be lost — then flag.
- **Highlight / colored text** — styling is dropped; text is preserved.
- **Checklists** — Apple checklist items often arrive as plain `<li>` bullets (no checkbox state in
  the exported body). They convert to plain `-` bullets. If a note is clearly a checklist and the
  user wants `- [ ]` task syntax, that's a per-note review decision — do not assume.

## Attachments / images (best-effort — v1)

The `body` HTML usually does **not** inline images; they live as separate attachment objects. For
each note the `.meta` file records `attachments <n>`.

- `attachments 0` → nothing to do.
- `attachments > 0` → **flag the note** in batch review. Best-effort: note that N attachment(s)
  exist so the user can decide whether to export them into `Sources/` and embed via
  `![[...]]`, or skip. Do not silently drop a note that has attachments — surface it.

## Source-language fidelity

Never translate. Whatever language the note used stays (Chinese stays Chinese, English stays
English). These cleanup rules touch **format only**, never wording. Same rule as `notion-import`.
