# Single source of truth — handling

The principle ("one concept = one representation") lives in `CLAUDE.md`. This file is the procedure for detection and resolution.

## What counts as a duplicate or conflict
- **Similar representations**: the same idea phrased differently — across notes, or within a single note (old version + updated version coexisting after an edit).
- **Conflicting representations**: incompatible claims about the same thing, whether across notes or within one note's history.

Both are forbidden — they cause misunderstanding later.

## Scope
Applies to: concepts, definitions, entities (people / tools / projects), factual claims, idea descriptions.

## Detection — search both ways before concluding "no existing representation"

Finding the existing representation is a **dual search** (see the 5-dimension judgment in `four-actions.md`): plaintext for exact terms — and for notes too recent to be in the RAG store — **plus** rag-search (semantic) for reworded duplicates plaintext misses. Neither alone is conclusive; run both before declaring a concept has no prior representation. Reindex stays manual — never refresh the store inside the capture turn.

## When updating existing content

Replace, don't accumulate. When updating a viewpoint, fact, or section:
- Rewrite the affected content in place. Do not leave the prior version commented out, struck through, or appended as "previously…".
- Remove redundancies that the edit introduces — duplicated phrasing, leftover transition sentences, stale cross-references.
- Audit trail lives in git history and the JSONL log, never in the note body.

Same principle, applied intra-note: one representation per concept, even across time.

## When you detect either
**Raise it immediately** — before writing, before saving, before moving on. Do not silently merge, reconcile, or pick one.

## How to raise
Present three things:
1. **Where** the existing representation lives (wikilink to the note).
2. **What** the overlap or conflict is (one or two sentences).
3. **Options** — typically: link to existing, merge, update the existing one, or rename if scopes actually differ.

Then let me decide.
