# Four Actions

Every vault change is one of four actions. Inflow has one action with two branches; Maintenance has two; Generation has one.

## Assimilation / Creation (Inflow)

One action, two branches. Triggered by Scribe at the user's explicit capture.

**One capture ≠ one action.** A single capture may contain several distinct concepts (e.g., a multi-concept document). Decompose first, then apply the judgment below to each concept independently — one capture can yield multiple actions, mixing Assimilation, Creation, and deferral. Each resulting action is its own atomic operation (`atomic-operation.md`): one edit, one log line, one commit.

- **Assimilation** — append to existing note.
- **Creation** — create a new atomic note inside `Notes/` (flat). Template selection per `templates.md`.

### 5-dimension judgment

Applied against candidate parent note(s) found by **dual vault search** — run both; they cover different blind spots:
- **Plaintext** — exact terms; also catches just-created notes the RAG store hasn't indexed yet (the store lags, by design).
- **rag-search (semantic)** — reworded / fuzzy duplicates plaintext misses; covers only already-indexed notes.

Neither alone is conclusive — RAG-empty ≠ no duplicate (store may lag); plaintext-empty ≠ no duplicate (wording differs). Plaintext runs on every capture; the semantic pass is **attempted before concluding Creation** (before declaring no existing note covers the concept) and whenever plaintext is inconclusive. RAG is **best-effort, not a hard gate** — if it's unavailable (`RAG_UNAVAILABLE`; see the rag-search skill's *Availability* section), plaintext-only is a valid fallback and capture proceeds; never block on RAG. Reindex is never triggered inside the capture turn — plaintext covers the lag.

| Dimension | Question |
|---|---|
| Semantic overlap | Does an existing note already cover this concept? |
| Structural fit | Does the new content slot naturally into a parent's existing sections? |
| Granularity match | Are new content and parent at the same abstraction level? |
| Substance distance | Does the new content alone pass concept-level Substance Test? |
| Reframing risk | Would appending change the parent's claim or scope? |

Resulting quadrants:

- Existing covers + not substantial → **Assimilation**.
- No coverage + substantial → **Creation**.
- Existing covers + substantial → SSOT risk; raise per `single-source-of-truth.md`. Possible resolutions: child concept gets its own note with wikilink to parent, or refinement of existing — the user decides.
- No coverage + not substantial → defer (no vault change).

### Tie-breaker

Only when the 5 dimensions are genuinely ambiguous: prefer the more reversible action — Assimilation + wikilink stub. Invocation requires `reason` to show per-dimension verdicts proving ambiguity. Defaulting to append without per-dimension reasoning is forbidden. See `atomic-operation.md`.

Substance Test reference: `substance-test.md`.

## Fission (Maintenance)

Trigger: a single note contains multiple concepts that should be separate atoms. Gardener-only.

**Two-layer test, both required for ≥2 sub-concepts inside the note**:

1. **Substance independence** — each sub-concept independently passes concept-level Substance Test (`substance-test.md`).
2. **Semantic independence** — agent drafts a minimal standalone note for each candidate. If the draft requires inlining another sub-concept's explanation to be coherent, semantic independence fails. Wikilink-only references are allowed.

Both AND'd. Pass → propose Fission.

Post-Fission disposition of the original note (hub vs full redistribution vs partial extract) is decided per case when the user confirms.

## Convergence (Maintenance)

Trigger: two notes describe the **same concept**. Detection and handling per `single-source-of-truth.md`. Gardener executes; Scribe surfaces SSOT issues at capture time but does not execute Convergence.

### Identity gate — similarity is a candidate signal, not a verdict

Semantic similarity (e.g. a rag-search hit, shared vocabulary) only *nominates* a pair. Before proposing Convergence, apply the concept-identity test:

> Would a knowledgeable reader say these two notes are trying to be the *same note*?

| Verdict | Condition | Action |
|---|---|---|
| **Same concept** | one note is a redundant or conflicting representation of the other (the duplicate/conflict of `single-source-of-truth.md`) | propose **Convergence** (merge) |
| **Distinct but related** | each has independent identity; only domain/vocabulary overlap | propose a **link** (a minimal Assimilation adding a `[[wikilink]]`) — **never a merge** |
| **Incidental** | shared words, no real relationship | **drop** — no proposal |

The link tier is the de-escalation path: it keeps similar-but-independent atoms separate (single source of truth) while still surfacing the relationship. It is **not a fifth action** — when approved it executes as a narrow Assimilation (append one `[[wikilink]]`). Reserve Convergence for genuine same-concept duplication; when in doubt between merge and link, prefer link (more reversible).

## Emergence (Generation)

Trigger: multiple existing notes share an implicit concept **never named anywhere** — not as a note title *and not as a wikilink target*. Gardener-only.

**Exclusion — a named stub is not Emergence.** A dangling `[[wikilink]]` (a target referenced across notes but not yet written) is *already named*, hence a Scribe **Creation-deferred stub** (`substance-test.md` fail-handling) — **out of Emergence scope, and out of Gardener scope entirely** (Gardener never proposes Creation). Emergence is only for the genuinely *implicit*: a theme recurring in note **prose** that no one has even linked yet.

**Test**: concept-level Substance Test on the implicit concept, using the existing notes mentioning it as material. Pass → propose. Fail → continue observing.

### Adjacency gate — a named *slice* is not a named *concept*

A candidate often brushes an existing note that names only *one application* of it — a domain-general principle whose narrower, domain-scoped instance already has a note. Adjacency is not coverage:

| Verdict | Condition | Action |
|---|---|---|
| **Emergent** | the general concept has no note of its own; existing notes name only slices/applications of it | propose **Emergence** — a new *parent* atom the slices are instances of |
| **Already covered** | the concept *as a concept* is already the subject of some note | **drop** — not Emergence (propose a link instead if a real relationship is unlinked) |

The new note must be the general principle, never a restatement of an existing slice (SSOT). Genuinely unsure which? Prefer **drop** + continue observing.

Defining sentence drafted by agent as probe; written by the user.

## Consumers

- Scribe: capture-time Assimilation/Creation; SSOT surfacing.
- Gardener auto-run: Fission, Convergence, Emergence detection.
