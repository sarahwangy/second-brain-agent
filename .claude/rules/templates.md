# Templates

Rules for Scribe's template handling during note creation. Gardener-side template work (template-emergence, refinement across vault) is out of scope for now.

## Template selection during Creation

When Scribe enters the Creation branch (per `four-actions.md`):

1. Identify the content shape — what kind of thing is being captured (a tool, a concept claim, a process, a decision log, a project, etc.).
2. Look at templates in `Templates/`. Match content shape against existing templates.
3. If a specialized template fits the shape → use it.
4. Otherwise → use `Templates/General Template.md` as fallback.

## Flagging template-candidate notes

When falling back to General Template, evaluate whether the content shape is reusable:

- Does the new note have clear sectional structure (not just freeform prose)?
- Does the structure plausibly repeat for similar future captures?

Both yes → flag to the user at confirm time:

> This note follows a [content-type] shape that could become a reusable template. Want to crystallize a new template after this note is saved?

Scribe does not auto-create templates. The user decides; if yes, template drafting happens as a separate follow-up turn (no rule for that flow yet — manual for now).

## Refinement signaling

When using a specialized template (not General Template fallback), if the note's actual content extends beyond the template's structure — new sections, frequently-empty fields, recurring deviations — flag the deviation to the user at confirm time:

> Note content extends beyond [template name] — added [new section / callout / element]. Future similar captures may suggest refining the template.

Scribe does not modify templates. The user decides whether to evolve the template based on accumulated signals (single-instance deviations are not sufficient on their own).

## Default

When in doubt, use General Template and proceed. Better to ship the note than stall on template selection.
