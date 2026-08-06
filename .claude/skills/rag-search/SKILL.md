---
name: rag-search
description: Vector-backed semantic / fuzzy retrieval over the Obsidian vault, plus the reindex that keeps the vector store in sync. Use the SEARCH path when the user wants to find notes by meaning rather than exact words — "what did I note about X", concepts worded differently than the query, or when plaintext search misses conceptually-relevant notes. Use the REINDEX path to refresh the gitignored vector store after notes change (manual; runs agent-semantic chunking). RAG COMPLEMENTS plaintext + Obsidian graph search — it does not replace them. Do NOT use for exact-string / detail lookups (plaintext search owns those), and never let vector similarity auto-write wikilinks (route any link suggestion through a Gardener proposal).
---

# RAG Search

## Overview

A vector store gives the vault **semantic / fuzzy retrieval** to complement plaintext search and the
Obsidian wikilink graph. Two paths:

- **Search** — embed a query, return nearest-neighbour note *parts*, rolled up to their parent note.
- **Reindex** — keep the store in sync after notes change. Chunking is **agent-semantic**: the agent
  (this session) decides how each changed note splits into parts; a Python script does the mechanical
  slice / embed / upsert.

The store lives in the gitignored `.rag-index/` — a **derived, rebuildable** projection of the notes.
Nothing is ever written into note frontmatter or body.

Scripts live in `.claude/skills/rag-search/scripts/`. Run them with the project venv: `.venv/bin/python`.

## When to use

- **Search path** — the user wants to find notes by *meaning*: "what did I write about X", a concept
  phrased differently than their wording, or when plaintext search came up empty on something that
  should exist. RAG **complements** plaintext + graph; interleave its hits with those, don't replace.
- **Reindex path** — notes were added / edited / deleted and the store should catch up before
  searching. Manual, on request — the store is not auto-synced, so capture stays instant.

Do **not** reach for RAG on exact-string or detail lookups — plaintext search owns those.

## Prerequisites

- venv deps installed (`lancedb`, `openai`, `python-dotenv`) — see `requirements.txt`.
- `.env` (copy from `.env.example`): `EMBED_PROVIDER=mock` runs offline for plumbing checks; real
  retrieval needs `EMBED_PROVIDER=api` plus a provider `base_url` / `api_key` / `model` / `dim`.
- First run needs a **reindex** to build the store.

## Availability — RAG is best-effort, degrade to plaintext

RAG is an **optional enhancement, never a hard dependency.** If it isn't configured (no `.env`,
`EMBED_PROVIDER=api` without a key), the params are wrong, the embedding API errors, or deps are
missing, the scripts emit a clean `RAG_UNAVAILABLE: <reason>` line instead of a traceback:

- **`search.py` exits 0 on failure** — treat `RAG_UNAVAILABLE` as "no RAG this turn": do **not**
  retry or surface an error; note it once and continue with **plaintext / grep only**. The workflow
  never blocks on RAG. (`RAG_UNAVAILABLE` ≠ `(no matches)` — the latter means RAG ran clean and found
  nothing.)
- **`reindex.py` exits non-zero on failure** — the store simply wasn't refreshed. Relay the reason to
  the user (usually a `.env` fix); don't retry blindly. (`plan` embeds nothing, so it still works with
  no embedder configured.)

**Every RAG consumer inherits this** — Scribe capture (dual search → plaintext-only), Gardener scan
(nominate via grep only), Discuss grounding. When RAG is down, reworded-duplicate detection weakens:
lean harder on plaintext term / synonym variations, and if SSOT confidence matters, suggest the user
configure RAG + reindex.

## Search path

Two steps: the vector store finds the semantic **entry points**; Obsidian **wikilinks** expand the
context around them. RAG does not store or compute the graph — relationships already live in the
notes' `[[wikilinks]]`.

**When to use it — and never guess:**
- Reach for vector search when the need is **fuzzy**, or when **plaintext search was inconclusive** —
  to *confirm* a match or *gather further context*, not as the first reflex for exact lookups.
- **Never guess.** If the retrieved parts don't clearly answer the query, say so and search further
  (more queries, wikilink expansion) or ask the user — never fabricate an answer or assert a match
  you're not sure of. Low confidence → surface it, don't paper over it.

**Reading confidence — distance is a signal, not just a rank:**
- Each hit's `_distance` (L2 on normalized vectors; smaller = stronger) tells you whether there's a
  *real* hit, not only the ordering.
- Read the shape, not a fixed number: one hit well below the rest, or hits concentrated in a single
  note → likely a real match; all distances clustered high and scattered across notes → noise.
- Early calibration anchors (text-embedding-3-large): a clear hit landed near ~0.82; a tangential
  "nothing really matches" landed near ~1.19. Rough guideposts, not cutoffs — recalibrate as queries
  accumulate.
- A weak top hit IS the "no strong match" case → trigger never-guess: say so, refine the query, or
  flag it as an unrecorded gap worth capturing.

**Agentic retrieval — run the loop, don't settle for round one:**

Search is a *loop this session runs*, not a single call. `search.py` is a stateless primitive; the
agent owns the iteration. Each round runs the two mechanics below (find entry points → expand via
wikilinks), then judges whether to stop or reformulate.

Per round:
1. **Search + read** — run `search.py` with the current query; read the hits via the distance guidance above.
2. **Judge sufficiency** — do the gathered parts (after wikilink expansion) actually answer the query / give
   enough context? Sufficient → stop. Not sufficient and budget remains → reformulate and loop.
3. **Reformulate deliberately** — choose the change from *why* the round fell short:
   - Weak, scattered hits (all distances high) → wrong vocabulary; rephrase toward the vault's likely wording / synonyms.
   - Compound question → decompose into sub-questions; search each separately.
   - Strong hit but missing surrounding context → expand via wikilinks (step 2 below), not a fresh vector query.
   - Too few hits → broaden; too noisy → narrow or add a qualifier.

**Stop as soon as any one holds:**
- **Sufficient** — the gathered parts answer the query.
- **Budget** — `SEARCH_MAX_ROUNDS` rounds done (default 3; set in `.env`, surfaced in each `search.py` run's footer).
- **Diminishing returns** — a round surfaces only already-seen parent notes (no new note enters the set); more rounds won't help.

**Across rounds** — track the set of parent notes already seen: dedup so the same note isn't re-reported, and so
the diminishing-returns check is meaningful.

**Stopping without sufficiency** (budget or diminishing-returns hit) — never-guess applies in full: present what you
found, state explicitly what's still missing, and offer to search differently or flag it as an unrecorded gap. Do not
manufacture closure to fill the gap.

**1. Find entry points** — embed the query, get the nearest-neighbour parts:

```bash
.venv/bin/python .claude/skills/rag-search/scripts/search.py "the query"
```

Each hit is a note part (parent `note_path` + `heading` + snippet + distance) — i.e. *which note,
which section* is semantically strongest.

**2. Expand context via wikilinks** — from each hit note, walk the graph with existing tools (no RAG
involvement):

- **Outgoing**: read the hit note, follow its `[[links]]`.
- **Backlinks**: plaintext-grep `[[<hit note>]]` for notes that reference it.

Present the **strong-match source text** plus its **wikilink neighbours**, as wikilinks to the parent
notes. Collapse multiple hits in the same note into one. RAG is one input — interleave with plaintext
results; it does not replace them.

## Reindex path (agent-semantic chunking)

Orchestrate three steps. The agent supplies only block-index ranges — it never emits note text, so
the note is preserved verbatim (`agent ≠ author`).

**Discipline — accuracy over speed (non-negotiable):**
- **Read every changed note in full before deciding its parts.** `plan` emits each note's complete
  block text — base the split on the actual content, never on headings or previews alone. Never
  chunk a note you haven't read.
- **Scale by staging, not by shortcutting.** If many notes changed (dozens to hundreds), do NOT
  chunk them all in one rushed pass — organize a staged plan and process in batches (read → decide →
  apply, batch by batch). Reduced throughput is an accepted trade-off; arbitrary chunking is not.
- **Never split arbitrarily.** Every boundary must come from understanding the content. When unsure
  how a note should split, slow down or ask — do not improvise a mechanical or guessed split.

**1. Plan** — detect changes and get each changed note's numbered blocks:

```bash
.venv/bin/python .claude/skills/rag-search/scripts/reindex.py plan
```

Returns JSON: `{"changed": [{"note_path", "content_hash", "blocks": [{index, type, title, section, text}]}], "deleted": [...]}`.

**2. Decide** — for each changed note, group its blocks into **parts** (contiguous block-index
ranges). Judgement:

- **Merge** strongly-related adjacent blocks into one part — don't hard-split a coherent train of thought.
- **Split** genuinely different directions / topics into separate parts.
- A short or single-concept (atomic) note → **one part** spanning all its content blocks.
- **Reference-list / index hubs → keep whole.** A note that's mostly `[[wikilinks]]` to other notes
  (an ideas index, a reading hub) → one part, not one-per-item: each item is a pointer to an
  already-indexed note, so splitting just makes noise.
- **A single usable unit → keep whole.** Content meant to be used as one piece (a complete prompt, a
  code block with its setup) stays in one part even if long — splitting it breaks it.
- **Ignore `frontmatter` blocks** — never put one in a part (metadata, not content).
- Parts must be **contiguous block ranges** covering the content blocks. Give only `[start, end]`
  index pairs — **never rewrite, summarise, or re-emit the text**.

**3. Apply** — pipe the decision to `apply`:

```bash
echo '{"notes":[{"note_path":"X.md","parts":[[1,3],[4,6]]}],"deleted":["Y.md"]}' \
  | .venv/bin/python .claude/skills/rag-search/scripts/reindex.py apply
```

`apply` slices each part verbatim by its block range, embeds it, and upserts; deletions are dropped.
It prints `{applied, deleted, parts}`.

**Fallback** — to rebuild without agent judgement (mechanical, splits by H1/H2/H3 section):

```bash
.venv/bin/python .claude/skills/rag-search/scripts/reindex.py auto
```

## Authority — defer to the rules, never restate them

This skill is RAG plumbing; the vault's judgement lives in the repo rules. The boundaries that keep
RAG compliant:

- **`atomic-operation.md` does NOT apply.** Reindex touches only the gitignored store — no markdown
  edit, no JSONL log, no commit, no four-action (same spirit as Gardener auto-run being read-only).
- **`single-source-of-truth.md`** — the store is a *derived projection* of the notes, always rebuilt
  from them; never a competing second representation. The note stays authoritative.
- **`linking.md`** — vector similarity is a *retrieval* aid only. It must **never** auto-write
  wikilinks or plain-text relationships. If similarity is used to *suggest* a link, route it through
  a user-approved Gardener proposal.
- **`substance-test.md` (agent ≠ author)** — chunking emits block *boundaries*, not text; the script
  slices verbatim. No content or meaning is altered, nothing added.

## Constraints

- **Derived, gitignored store** — `.rag-index/` is rebuildable; never committed, never the source of truth.
- **Complements, never replaces** plaintext + graph search.
- **Agent gives ranges, not text** — reindex never alters a note.
- **Manual reindex** — not inside the capture turn; the store is allowed to lag until refreshed.
- **No auto-linking** from similarity — suggestions go through Gardener, never a silent write.
