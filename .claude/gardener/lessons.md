# Gardener Lessons

Distilled, **pattern-level** self-correction memory for the Gardener agent. Gardener reads this at the start of every run and treats each lesson as an extra constraint on proposal generation, layered on top of the four-actions rules.

## Relationship to the log (don't duplicate it)

| Source | Holds | Question it answers | Altitude |
|---|---|---|---|
| `.claude/log/changes.jsonl` | every concrete proposal + outcome + `decision_note` | "don't re-propose **this** item" | event-level |
| this file | heuristics distilled from repeated rejections/corrections | "don't repeat **this class** of mistake" | pattern-level |

The log is the raw ledger; this file is the synthesis. Anti-repeat greps the log; behavioral self-correction reads this. Complementary — never copy log rows here.

## Write protocol

- **Who** — the **main session** writes here. The Gardener sub-agent is read-only and never edits this file.
- **When** — only when a rejection (or correction) reveals a *generalizable, repeatable* pattern. A one-off decline with no transferable lesson stays in the log only. Do **not** append a lesson per rejection — that bloats the file into noise.
- **SSOT** — one lesson per pattern. A new lesson that refines or contradicts an existing one **replaces it in place**; do not accumulate stale or conflicting lessons. The audit trail lives in git history + the JSONL log, not here.
- **Scope** — Gardener-only for now. Generalize to Scribe later only if the need appears.

## Lesson format

```
### L<n> — <short imperative title>
**Heuristic**: <what to do / not do, in one line>
**Why**: <the rejection rationale or correction that motivated it>
**Origin**: <YYYY-MM-DD · log target(s) or short ref>
```

## How Gardener uses it

At startup, read this file. For each candidate proposal, check it against every lesson here *before* surfacing — a lesson is a veto/adjust signal of equal weight to the anti-repeat log check. If a lesson would suppress a proposal, skip it (or down-tier per the lesson) and note the suppression in the run summary.

## Lessons

*(none yet — seeded empty; the first lesson lands when a rejection reveals a repeatable pattern)*
