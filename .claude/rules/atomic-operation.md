# Atomic Operation

Every vault modification — by Scribe or Gardener — must complete the following three steps in a single agent turn.

## The three steps

1. Edit / create / delete the markdown file(s).
2. Append a JSONL line to `.claude/log/changes.jsonl` per `log-schema.md`.
3. `git add -A && git commit -m "<message>"` with the format defined in `log-schema.md`.

If any step fails, the turn is incomplete. Surface the failure to the user; do not retry partial.

## Reasoning visibility (hard constraint)

Step 2's `reason` field must contain the agent's per-dimension reasoning specific to the action.

- **Assimilation / Creation**: explicit verdict on each of the 5 dimensions (Semantic overlap / Structural fit / Granularity match / Substance distance / Reframing risk) plus the branch decision.
- **Concept-level Substance Test** (Creation / Emergence / Fission): draft defining sentence + sub-topic candidate with source traces.
- **Tie-breaker invocation**: dimension-by-dimension reasoning showing genuine ambiguity. "Defaulting to append because reversible" is forbidden. See `four-actions.md`.

The user verifies the work via `reason` at confirm time. Gardener uses it for anti-repeat.

## Session-start recovery

At the start of every Scribe session or Gardener execute-mode session, run `git status`. Dirty working tree → previous operation interrupted → surface to the user before any new action. The user decides commit / rollback / discard.

## Read-only

Gardener auto-run is read-only; it writes nothing — neither markdown nor log. Atomic operation does not apply.
