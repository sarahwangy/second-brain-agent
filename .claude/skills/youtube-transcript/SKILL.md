---
name: youtube-transcript
description: This skill should be used when the user provides a YouTube URL or video ID and wants the agent to extract, summarize, or discuss the video's content. Because the agent cannot watch video, it works from the transcript — fetched via a bundled script (youtube-transcript-api, run through uv), then context-corrected for caption errors and summarized. Do NOT use for non-YouTube media, or when no video is referenced.
---

# YouTube Transcript

## Overview

Turn a YouTube URL into usable knowledge: fetch the transcript, correct caption errors from context, and summarize — then discuss it or hand off to vault capture. The agent cannot watch video, so the transcript is the only source.

## When to use

Trigger when the user provides a YouTube URL or video ID and wants its content extracted, summarized, or discussed. Do not trigger for non-YouTube media or when no video is referenced.

## Requirements

`uv` must be installed. No manual Python setup is needed: the bundled script declares its own dependency via PEP 723 inline metadata, so `uv run` provisions a cached ephemeral environment on first run. Network is required on the first fetch.

## Workflow

### 1. Fetch the transcript

Run the bundled script with the URL or ID — it extracts the video ID and prints the transcript:

```bash
uv run .claude/skills/youtube-transcript/scripts/fetch_transcript.py "<url-or-id>" --timestamps
```

Options: `--languages en,zh` (preferred languages in order; falls back to any available), `--timestamps` (prefix `[mm:ss]`), `--json` (raw snippets with start/duration).

If the script exits non-zero (no captions, transcripts disabled, video unavailable, network/rate-limit), report the specific failure to the user. Never fabricate the video's content.

### 2. Correct transcript errors before using it

Auto-generated captions are error-prone. Before summarizing or capturing, reconstruct intended meaning from context — do NOT treat the transcript as ground truth:

- **Homophones / mishearings** — "their/there", "to/two"; brand and technical terms transcribed phonetically.
- **Missing punctuation / segmentation** — run-on text; infer sentence boundaries.
- **Dropped or duplicated words** — common in fast or accented speech.

Use surrounding context and domain knowledge to infer the true wording. Where a correction is uncertain and material, flag it to the user rather than asserting it as fact.

### 3. Summarize

Produce a faithful summary of the corrected content. Attribute claims to the video; keep the agent's own knowledge separate.

### 4. Discuss or capture

Present the summary, then follow the user's intent:

- **Discuss** (default) — answer and explore per the `CLAUDE.md` Scribe role. No vault changes.
- **Capture** — only on explicit capture intent. Route through the four-actions flow (`.claude/rules/four-actions.md`), mirroring `pdf-to-notes`: a source/hub note for the video plus the atomic concept notes it spawns, linked by wikilinks. (Dedicated YouTube source-note template + capture wiring is a planned follow-up; until then, apply the existing capture rules directly.)

## Constraints

- **Transcript ≠ truth** — always context-correct before relying on it.
- **No fabrication** — if the transcript cannot be fetched, say so; never invent content.
- **Defer to the rules** — all capture judgment lives in the repo rules; this skill references them, never restates them.
