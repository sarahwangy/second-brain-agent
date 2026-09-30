# Agent Blueprint — Jarvis (Personal Knowledge Base Agent System)

**Version:** 1.0 · **Owner:** Sarah Wang · **Status:** In production use (personal, self-hosted)
**Related artefacts:** [`CLAUDE.md`](./CLAUDE.md) · [`.claude/rules/`](./.claude/rules) ·
[`.claude/agents/gardener.md`](./.claude/agents/gardener.md) ·
[`.claude/log/changes.jsonl`](./.claude/log/changes.jsonl)

---

## 1. Purpose

Jarvis is a two-agent system that maintains a personal Obsidian knowledge base (notes, wikilinks,
git-versioned). The design problem it solves is not "can an agent write notes for me" — a single
agent can do that trivially — but **how to let an agent perform ongoing structural maintenance
(merging, splitting, cross-linking notes) without it being able to silently corrupt the knowledge
base**, and with every change traceable to a decision a human actually made.

This document describes the agent roster, autonomy boundaries, human checkpoints, audit
mechanism, and failure-mode handling as a standalone blueprint — the pattern is domain-agnostic
and is written here in a form reusable outside this specific project.

## 2. Agent Roster

| Agent | Role | Can write? | Invocation |
|---|---|---|---|
| **Scribe** | Daily conversational driver. Captures notes on explicit user request; owns scope, approval, execution and logging for every session. | Yes — only on explicit capture intent, never inferred | Every session (default) |
| **Gardener** | Periodic structural maintenance analyst. Scans the vault, proposes Fission / Convergence / Emergence / link opportunities. | **No — hard-enforced read-only** | On explicit user request only ("run Gardener") — never auto-invoked |

## 3. Autonomy Boundary

The core control is: **the agent that can see the most (Gardener, full-vault scans) is the agent
that can change the least (nothing).** Execution authority sits only with Scribe, and only after a
human has approved a specific action.

| Action | Gardener | Scribe |
|---|---|---|
| Read / scan vault | ✅ | ✅ |
| Propose a structural change | ✅ (report only) | — |
| Write / edit a note | ❌ (hard constraint — no mutating file or git operations of any kind) | ✅, only on explicit capture or an approved Gardener proposal |
| Execute a Gardener proposal | ❌ | ✅ (on the user's behalf, per-proposal) |
| Refresh the semantic search index | ❌ (search-only, never reindex) | manual, outside capture flow |
| Self-approve a change | ❌ (not a real option — no write path exists) | ❌ (approval is always the user's, never inferred) |

Gardener's constraint is enforced at the tool level, not just by instruction: its tool grant is
`Read, Grep, Glob, Bash, Skill` — no file-write or git-mutation tool is available to it at all, and
it is explicitly forbidden from running any mutating Bash command (no redirects, no `git
add/commit/restore/stash`, no `mv/rm/cp/touch/tee/sed -i`). The boundary does not depend on the
model choosing to comply.

## 4. Human-in-the-Loop Checkpoints

1. **Scope gate** — before any Gardener run, the human sets scope (full-vault or a bounded
   region). Gardener never widens scope on its own.
2. **Per-proposal approval** — every Gardener proposal is presented individually, with its
   reasoning visible, and approved or rejected one at a time. Nothing executes in batch.
3. **Rejection is a first-class outcome, not a dead end** — a rejected proposal is logged with the
   user's own stated reason (`decision_note`). If a rejection reveals a repeatable pattern, it gets
   distilled into a standing lesson so Gardener stops re-proposing the same category of change.

## 5. Audit & Traceability

Every write, by either agent, completes an **atomic operation**: (1) the file edit, (2) one JSONL
log line, (3) one git commit — as a single unit. If any step fails, the operation is treated as
incomplete and surfaced to the user; there is no silent partial retry.

Each log entry records: timestamp, which agent proposed it, which of the four defined actions it
is (Assimilation / Creation / Fission / Convergence / Emergence), the targets affected, the
**per-dimension reasoning** behind the decision (not just the outcome), whether it executed or was
rejected, and — for rejections — the human's own rationale in their own words. This is what makes
the log usable for both audit (why did this change happen) and for the agent's own anti-repeat
check (has this exact proposal already been declined, and why).

## 6. Failure Modes & Runbook

| Failure mode | Detection | Response |
|---|---|---|
| Prior operation interrupted mid-write (dirty git tree at session start) | `git status` run at the start of every session, before any new action | Surface to the user; they decide commit / rollback / discard before anything new proceeds |
| Semantic search index stale or unavailable | Checked before a Gardener run | Search still proceeds on plaintext/grep alone (best-effort, never a hard gate); staleness is flagged in the report rather than silently ignored |
| Gardener re-proposing something the user already rejected | Anti-repeat check against logged `rejected` entries before surfacing any new proposal | Skip; if rejected repeatedly for the same target, escalate to the user instead of re-proposing |
| Ambiguous merge-vs-link decision between two similar notes | Explicit "would a knowledgeable reader call these the same note?" identity test | When genuinely ambiguous, default to the more reversible option (link, not merge) |

## 7. Governance Notes

- **Reversibility as a default heuristic**: whenever a decision is genuinely ambiguous, the system
  is designed to prefer the more reversible outcome (a link over a merge, an Assimilation over a
  Creation) rather than defaulting to whichever looks more impressive.
- **No silent self-correction**: the system never merges conflicting content or resolves a
  duplicate/conflict on its own — it raises the conflict to the human with the two representations
  and the available options, and lets them decide.
- **Reasoning must be inspectable, not just the outcome**: "why" is a first-class, structured field
  in every log entry, not a free-text afterthought — this is what makes the audit trail actually
  auditable rather than just a change list.

## 8. Reuse Notes (what generalizes beyond this project)

The pattern that would carry over to an enterprise agent catalogue entry is: separate the
**highest-visibility, highest-change-surface** agent role (full-scan analysis) from **execution
authority**, enforce that separation at the tool-permission layer rather than the prompt layer,
require structured per-decision reasoning in the audit log rather than a bare outcome, and make
rejection (not just approval) a logged, reusable signal.
