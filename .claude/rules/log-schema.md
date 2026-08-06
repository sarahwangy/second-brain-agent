# Log Schema

JSONL append-only ledger at `.claude/log/changes.jsonl`. Records every vault modification and every Gardener proposal decision. Used by Gardener for anti-repeat, by the user for audit (mirrored in git commit messages).

## Entry format

```jsonl
{
  "timestamp": "ISO8601",
  "agent": "scribe" | "gardener",
  "action": "Assimilation" | "Creation" | "Fission" | "Convergence" | "Emergence",
  "targets": ["note title or path", ...],
  "reason": "per-dimension reasoning required by the action's rule",
  "outcome": "executed" | "rejected",
  "decision_note": "the user's rationale for the decision — required when rejected",
  "decided_by": "the user"
}
```

## Field notes

- `targets`: note titles or paths affected. Multiple entries when an action spans notes (e.g., Convergence merges two).
- `reason`: must include the per-dimension reasoning specific to the action — 5-dim breakdown for Assimilation/Creation, substance-test drafts for concept-level decisions, self-contained rewrite test for Fission. See `four-actions.md`.
- `outcome`: two states only. `executed` = vault changed. `rejected` = Gardener proposal the user declined (vault unchanged, log + commit only). Pending proposals live in chat, not in log.
- `decision_note`: the user's own rationale for the decision, in their framing — distinct from `reason` (the agent's proposal logic). **Required when `outcome` is `rejected`** so every decline is traceable; optional on `executed` (record only when the user added a notable instruction or modification). A rejection whose rationale reveals a *repeatable pattern* may also be distilled into `.claude/gardener/lessons.md` (event-level here, pattern-level there).
- `decided_by`: always `the user`. Agents never self-approve.

## Writing patterns

| Agent / mode | Log entries written |
|---|---|
| Scribe | 1 per executed action |
| Gardener auto-run | 0 (proposals stay in chat) |
| Gardener execute mode | 1 per acted-on proposal — `executed` or `rejected` |

Under the Claude Code sub-agent implementation, the Gardener sub-agent is **always read-only** (writes 0 entries, like auto-run). When the user approves or rejects a Gardener proposal in the interactive session, the **main session writes the entry on the sub-agent's behalf**, with `agent: "gardener"` (it is a Gardener-class action regardless of which layer holds the pen). See `.claude/agents/gardener.md`.

## Anti-repeat

Before generating any new proposal, Gardener greps `outcome: rejected` entries and uses semantic judgment (not string equality) to decide if the candidate is materially the same as a previously rejected one. Match → skip. Repeated rejections for the same target → flag to the user rather than re-propose.

## Git commit alignment

Every log entry corresponds to one git commit (see `atomic-operation.md`). Commit message format:

```
[<outcome>] <action>: <targets> | <short reason>
```
