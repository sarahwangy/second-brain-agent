---
name: pdf-to-notes
description: This skill should be used when the user provides a PDF and explicitly asks to capture, ingest, or turn it into notes in the Obsidian knowledge base (e.g. "summarize this PDF and make notes", "add this paper to my vault"). It orchestrates the Scribe ingestion flow — read the PDF, create one source/hub note, decompose the document into atomic concept notes via the vault's four-actions judgment, store the original in Sources/, and commit one action at a time. Do NOT use for merely reading or discussing a PDF with no capture intent, nor for non-PDF captures.
---

# PDF to Notes

## Overview

Ingest a single PDF into the Obsidian vault as a **source/hub note** plus the **atomic concept notes** it spawns, all connected by wikilinks. This skill is a thin orchestration: it sequences the move but defers every judgment to the vault's existing rules — it never restates them.

## When to use

Trigger only when BOTH hold:

- The capture target is a **PDF** (provided as a file or already in the vault).
- The user has expressed **explicit capture intent** — Manage mode per `CLAUDE.md` requires it.

Reading or discussing a PDF with no capture intent is Discuss mode. Do not trigger.

## Authority — defer to the rules, never restate them

The canonical judgment lives in the repo rules. Read and apply them in place; do not duplicate their content here.

- `CLAUDE.md` — Scribe modes, vault principles, confirmation gates.
- `.claude/rules/four-actions.md` — Assimilation/Creation judgment; "one capture ≠ one action".
- `.claude/rules/substance-test.md` — concept-level threshold for a new note.
- `.claude/rules/single-source-of-truth.md` — duplicate/conflict detection.
- `.claude/rules/templates.md` — template selection.
- `.claude/rules/atomic-operation.md` + `.claude/rules/log-schema.md` — 3-step write, JSONL log, one commit per action.
- `.claude/rules/linking.md` — wikilink decisions.

## Workflow

### 1. Read the PDF

Use the built-in Read tool. For PDFs over 10 pages, read in page ranges (max 20 pages per call) until the whole document is covered.

### 2. Summarize the whole document

Produce a distilled overview of the entire PDF — this becomes the source note's Summary. Use only the PDF's content; keep outside knowledge out (per the Substance Test's allowed-sources rule).

### 3. Decompose into distinct concepts

List the separable concepts the PDF contains. Atomicity governs: one PDF yields many notes, never one mega-note. Do not force every section into a note — the Substance Test decides which concepts qualify (step 6).

### 4. Confirm scope with the user

Before any write, surface: the proposed source-note title, the list of candidate concepts, and which look like new notes vs appends to existing notes. Get explicit confirmation. Confirm title / location / template per `CLAUDE.md`.

### 5. Create the source note

- Store the original PDF in `Sources/` (gitignored by design — kept locally, not committed).
- Create one source note from `Templates/PDF Source Note.md`. Fill `{{title}}`, `{{date}}`, the `![[Sources/...]]` embed, `url` (if any), and the Summary.
- Leave the **Spawned notes** section to be filled as concept notes are created (step 6).

### 6. Process each concept through the four actions

For **each** concept independently:

- Run the 5-dimension judgment (`four-actions.md`) against vault-search candidates → Creation, Assimilation, SSOT-raise, or defer.
- Apply the concept-level Substance Test (`substance-test.md`) before any Creation.
- On any duplicate/conflict, stop and raise per `single-source-of-truth.md` — never silently merge.
- For each created/updated note, wikilink it **back** to the source note and list it under the source note's **Spawned notes**. Many-to-many holds: a concept synthesizing several PDFs links to several source notes.

### 7. Commit one action at a time

Each note creation/append is its own atomic operation (`atomic-operation.md`): one edit, one JSONL log line with per-dimension reasoning (`log-schema.md`), one commit. The source note is itself one such action.

## Constraints

- **Agent ≠ author** — draft defining sentences are probes; the user writes the final wording.
- **Relationships are wikilinks only** — never inline-copy content between notes (`single-source-of-truth.md`, `linking.md`).
- **Confirmation-gated** — no vault write without explicit user capture confirmation.
