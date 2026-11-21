---
description: "Revise the feature's spec.md to address the violations in epic-review.md, then show what changed"
---

# EPIC Revise

Rewrite the current feature's `spec.md` to address the violations recorded in `epic-review.md`, following EPIC's authoring rules, and show the person exactly what changed. This command changes **only `spec.md`**. It never changes code, `plan.md`, `tasks.md`, or the review itself.

## User Input

```text
$ARGUMENTS
```

The input is optional. It may contain:

- A feature directory (for example `specs/001-user-login`). If absent, use the current feature.
- Violation numbers to apply (for example `V-001 V-020 V-023`). If absent, apply all violations.
- `--high-only`: apply only violations marked `Confidence: high`.

## Reference material

- `.specify/extensions/epic-framework/references/epic-skill.md`: read the **"Writing and revising artifacts"** section. It is the rulebook for this command.
- `.specify/extensions/epic-framework/references/practices.md`: full practice definitions, for deciding what a compliant passage looks like.

## Step 1: Find the inputs

1. Resolve `FEATURE_DIR`: use the directory given by the user, otherwise `feature_directory` from `.specify/feature.json`. If neither exists, tell the user and stop.
2. Require `FEATURE_DIR/spec.md` and `FEATURE_DIR/epic-review.md`. If the review is missing, tell the user to run the EPIC review command first, and stop.
3. Read both files, plus the EPIC references above.
4. Select the violations to apply, using the user input (specific V-numbers, `--high-only`, or all). Only violations whose **Location** is in `spec.md` can be applied. Violations located in other files (checklists, constitution, missing plan or tasks) are skipped and listed as skipped.
5. If `epic-review.md` looks older than the current `spec.md` (quotes in the review no longer appear in the spec), warn the user that the review may be stale and ask whether to continue. Skip any violation whose quote is no longer in the spec.

## Step 2: Back up the current spec

Before changing anything, copy `FEATURE_DIR/spec.md` to `FEATURE_DIR/spec.before-epic-revise.md`, replacing any older backup. This is the "before" version for the diff and lets the person undo the revision.

## Step 3: Revise

For each selected violation, make the **smallest change** to `spec.md` that resolves it, following these rules:

- **Do not guess at decisions the person has not made.** If resolving a violation needs a value, threshold, scope choice, or behavior that is not already stated somewhere in the artifacts, insert a marker instead, for example `[NEEDS CLARIFICATION: reset link validity window?]`. An invented number reads as a requirement and will be implemented as one.
  - If the value already exists elsewhere in the spec (for example a number in a success criterion or assumption), you may move or repeat it into the requirement, and say where it came from.
- **Keep existing IDs.** Never renumber. When splitting a compound requirement, use sub-letters (`FR-004` becomes `FR-004a`, `FR-004b`, ...). New entries get the next unused number.
- **Keep the Spec Kit template.** Do not remove or reorder mandatory sections.
- **Keep behavior, not mechanism.** When moving implementation detail out of the spec (C1), restate the requirement as an observable property, and add a `[NEEDS CLARIFICATION]` or a note that the mechanism belongs in the plan. Do not create `plan.md`.
- **Do not add new scope.** Only resolve the listed violations.
- **Missing content** (for example missing failure behavior): add the requirement or scenario if its behavior is clear from the spec; otherwise add a `[NEEDS CLARIFICATION]` stating the open question.

## Step 4: Show what changed

1. Show a diff between `spec.before-epic-revise.md` and the new `spec.md`. If `git` is available, `git diff --no-index -- <before> <after>` works even outside a repository. Otherwise show the changed passages as before/after pairs.
2. Write a change log to `FEATURE_DIR/epic-revise-log.md`:

```markdown
# EPIC revise log: <feature name>

**Date:** <YYYY-MM-DD>
**Review used:** epic-review.md
**Backup of previous spec:** spec.before-epic-revise.md

## Applied

| Violation | Practice | Location | Change |
|---|---|---|---|
| V-001 | E1.2 | FR-015 | Moved "10 attempts per 15 minutes" from SC-006 into FR-015 |

## Needs a decision

| Violation | Marker added | Question |
|---|---|---|
| V-002 | FR-012 | Reset link validity window? |

## Skipped

| Violation | Reason |
|---|---|
| V-060 | Located in checklists/requirements.md, not spec.md |
```

## Guardrails

- The only files this command writes are `spec.md`, `spec.before-epic-revise.md`, and `epic-revise-log.md`.
- Never modify code, `plan.md`, `tasks.md`, checklists, the constitution, or `epic-review.md`.
- Never invent values. Use `[NEEDS CLARIFICATION]`.
- Never renumber existing IDs.

## Completion

Tell the user:

- How many violations were applied, how many need a decision, and how many were skipped.
- The path to the change log and the backup.
- How to undo: copy `spec.before-epic-revise.md` back over `spec.md`.
- Suggest running the EPIC review command again to check the revised spec.
