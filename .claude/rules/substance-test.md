# Substance Test

The single judgment criterion for whether a concept deserves its own structure (wikilink, note, section). Used by both Scribe and Gardener.

## The test

> Does this concept have room to grow — background, sub-topics, examples, evolution potential?

Same question, two thresholds.

## Phrase-level — low bar, forward-looking

For wikilink decisions inside note text. Pass if the concept *could plausibly* grow into a note someday. Stub links acceptable. See `linking.md` for link-specific application.

## Concept-level — high bar, present-tense

For creating new notes (Creation / Emergence) or splitting (Fission).

**Pass condition**: agent must produce, using only material already present, both:
1. A defining sentence for the concept
2. At least one sub-topic candidate

**Allowed sources**: current capture content + existing vault notes the agent has read.
**Forbidden sources**: agent's training knowledge — anything not traceable to vault or capture is hallucination for this test.

**Fail handling**: candidate stays as wikilink stub or plain text. Re-evaluate on future passes when more material accumulates.

Drafts are probes, not final content — the user writes the final defining sentence (agent ≠ author principle).

## Application

| Decision | Threshold | Owner |
|---|---|---|
| Wikilink a term in note text | Phrase | \`linking.md\` |
| Assimilation / Creation: append vs new note | Concept | \`four-actions.md\` |
| Fission: split sub-concept out | Concept | \`four-actions.md\` |
| Emergence: implicit theme → note | Concept | \`four-actions.md\` |
| Capture nudge during Discuss/Brainstorm | Concept | \`CLAUDE.md\` Scribe role |

## Reasoning visibility

Concept-level applications must include the draft defining sentence + sub-topic candidate in the \`reason\` field of the resulting log entry (see \`log-schema.md\`).
