---
description: "Report the parts of the current feature's spec, plan, and tasks that violate EPIC practices, then optionally revise spec.md to address them"
---

# EPIC Review

Check the current feature's Spec Kit artifacts against the EPIC framework and write a report of the parts that **violate** EPIC practices. The report itself never proposes fixes. After the report, the command asks whether to apply fixes to `spec.md`, and only changes `spec.md` if the user says yes or passed `--revise`.

## User Input

```text
$ARGUMENTS
```

The input is optional. It may contain:

- A feature directory (for example `specs/001-user-login`). If absent, use the current feature.
- `--score`: also include the 0–3 dimension scores. Without it, the report lists violations only.
- `--revise`: after writing the report, apply the fixes without asking (the same as answering "yes"). It can be followed by `high-only` or a list of V-numbers (for example `--revise high-only` or `--revise V-001 V-004`) to limit which violations are applied.

## Reference material

The EPIC definitions live next to this command, in the installed extension:

- `.specify/extensions/epic-framework/references/epic-skill.md`: the EPIC categories, dimensions, rubric, and the 40 practices in short form. Its **"Writing and revising artifacts"** section is the rulebook for the revise step.
- `.specify/extensions/epic-framework/references/practices.md`: full definitions, signals, and examples for each practice.

Read both before reviewing. Use them as the **only** source for what counts as a violation. Do not invent rules that are not in EPIC.

For the report (Steps 3 and 4), ignore the "Writing and revising artifacts" section and the "Recommended revisions" part of the output template in `epic-skill.md`. The report does not revise.

## Step 1: Find the feature

1. If the user gave a feature directory, use it.
2. Otherwise read `.specify/feature.json` and use its `feature_directory`.
3. If neither exists, tell the user to run the specify command first, and stop.

Set `FEATURE_DIR` to that directory.

## Step 2: Collect the artifact set

Read every file that exists among:

- `FEATURE_DIR/spec.md` (required: stop if missing)
- `FEATURE_DIR/plan.md`, `tasks.md`, `research.md`, `data-model.md`, `quickstart.md`
- `FEATURE_DIR/contracts/` and `FEATURE_DIR/checklists/`
- `.specify/memory/constitution.md`

Record which files were read and which are absent. An unfilled template (for example a constitution still containing `[PRINCIPLE_1_NAME]` placeholders) is not evidence; say so.

## Step 3: Review independently

The review must be a **fresh check**, not influenced by whoever wrote the artifacts.

- If your agent can start an independent sub-agent, delegate Steps 3 and 4 to it. Give it only: the list of artifact paths, the two reference file paths, and the rules in this command. Do **not** pass it the conversation history.
- If it cannot, base the review **only** on the file contents. Ignore anything said earlier in this conversation about why the artifacts were written the way they were.

Then:

1. Read the whole artifact set once before judging anything.
2. For each of the ten dimensions (E1, E2, E3, P1, P2, I1, I2, I3, C1, C2), look for places where a practice is violated: vague terms, compound requirements, missing verification, contradictions, misplaced content, and so on, as defined in the references.
3. For each violation, record:
   - **Practice**: the practice ID and name (for example `E1.2 Quantified / Measurable Requirements`)
   - **Location**: the file and the most specific anchor available (requirement ID such as `FR-015`, success criterion `SC-006`, user story `US2`, section heading, or line)
   - **Quote**: the exact text from the artifact. For something missing, write `(missing)` and name where it was expected.
   - **Why**: one or two sentences on how it violates the practice, and what an implementing agent would have to guess.
4. Report only what is actually in the files. Quote verbatim. If you are unsure whether something is a violation, include it with `Confidence: low` rather than dropping it or overstating it.
5. Do not report a practice as violated when it does not apply to this feature (for example E2.5 when no sensitive data is handled). List those under "Not applicable".
6. Absent files (for example no `plan.md` yet) are reported once under "Missing artifacts", not repeated as many separate violations.

## Step 4: Write the report

Write to `FEATURE_DIR/epic-review.md`, replacing any previous EPIC review there. Use this structure:

```markdown
# EPIC review: <feature name>

**Date:** <YYYY-MM-DD>
**Artifacts reviewed:** <files>
**Missing artifacts:** <files, or "none">
**Violations found:** <n> (E <n> | P <n> | I <n> | C <n>)

## Violations

### E1 Unambiguous

**V-001**: E1.2 Quantified / Measurable Requirements
- Location: spec.md, FR-015
- Quote: "after a threshold of consecutive failures"
- Why: <how it violates the practice>
- Confidence: high | medium | low

<Repeat for each violation, numbered V-001, V-002, ... in dimension order E1, E2, E3, P1, P2, I1, I2, I3, C1, C2. Omit a dimension heading if it has no violations.>

## Missing artifacts

- <file>: <which dimensions cannot be fully assessed without it>

## Not applicable

- <practice ID>: <why it does not apply>

## Notes

- This report lists violations only. It does not propose fixes.
- EPIC findings are judgments by an AI reviewer and are not calibrated against human raters. Check the quotes.
```

If `--score` was given, add a `## Scores` table after the header with each dimension's 0–3 score from the EPIC rubric and the total out of 30.

Report rules:

- While reviewing and writing the report, **never modify** `spec.md`, `plan.md`, `tasks.md`, or any other artifact. The only file Steps 1–4 write is `FEATURE_DIR/epic-review.md`.
- **The report never proposes fixes**: no "Recommended revisions", no rewritten requirements, no suggested wording.
- **Never quote text that is not in the artifacts.**
- Phrase findings about the artifacts, not about the people who wrote them.

## Step 5: Report and ask

Tell the user:

- The path to `epic-review.md`
- The number of violations per category (E, P, I, C)
- The three violations most likely to make an implementing agent guess, by V-number

Then decide whether to revise:

- **If `--revise` was given**: do not ask. Go to Step 6 with the selection given after `--revise` (`high-only`, a list of V-numbers, or all violations if nothing follows).
- **Otherwise, ask:**

  > Want me to apply these fixes to spec.md? (yes / no / list of V-numbers / high-only)

  - **No**: stop. Tell the user they can run this command again with `--revise` later.
  - **Yes**, a list of V-numbers, or `high-only`: go to Step 6 with that selection.
- **In automated or non-interactive mode without `--revise`**: do not ask and do not revise. Stop after the report.

Run Step 6 in the main session, not a sub-agent, so the user sees the diff.

## Step 6: Revise spec.md (only after "yes" or `--revise`)

### 6.1 Select the violations

Apply the selection from Step 5: specific V-numbers, `high-only` (only violations marked `Confidence: high`), or all. Only violations whose **Location** is in `spec.md` can be applied. Violations located in other files (checklists, constitution, missing plan or tasks) are skipped and listed as skipped.

### 6.2 Back up the current spec

Before changing anything, copy `FEATURE_DIR/spec.md` to `FEATURE_DIR/spec.before-epic-revise.md`, replacing any older backup. This is the "before" version for the diff and lets the user undo the revision.

### 6.3 Revise

For each selected violation, make the **smallest change** to `spec.md` that resolves it, following these rules:

- **Do not guess at decisions the user has not made.** If resolving a violation needs a value, threshold, scope choice, or behavior that is not already stated somewhere in the artifacts, insert a marker instead, for example `[NEEDS CLARIFICATION: reset link validity window?]`. An invented number reads as a requirement and will be implemented as one.
  - If the value already exists elsewhere in the spec (for example a number in a success criterion or assumption), you may move or repeat it into the requirement, and say where it came from.
- **Keep existing IDs.** Never renumber. When splitting a compound requirement, use sub-letters (`FR-004` becomes `FR-004a`, `FR-004b`, ...). New entries get the next unused number.
- **Keep the Spec Kit template.** Do not remove or reorder mandatory sections.
- **Keep behavior, not mechanism.** When moving implementation detail out of the spec (C1), restate the requirement as an observable property, and add a `[NEEDS CLARIFICATION]` or a note that the mechanism belongs in the plan. Do not create `plan.md`.
- **Do not add new scope.** Only resolve the selected violations.
- **Missing content** (for example missing failure behavior): add the requirement or scenario if its behavior is clear from the spec; otherwise add a `[NEEDS CLARIFICATION]` stating the open question.

### 6.4 Show what changed

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

### 6.5 Revise rules

- The only files Step 6 writes are `spec.md`, `spec.before-epic-revise.md`, and `epic-revise-log.md`.
- Never modify code, `plan.md`, `tasks.md`, checklists, the constitution, or `epic-review.md`.
- Never invent values. Use `[NEEDS CLARIFICATION]`.
- Never renumber existing IDs.

### 6.6 Tell the user

- How many violations were applied, how many need a decision, and how many were skipped.
- The path to the change log and the backup.
- How to undo: copy `spec.before-epic-revise.md` back over `spec.md`.
- If any `[NEEDS CLARIFICATION]` markers were added, suggest answering them with `/speckit-clarify`, then running this command again to check the revised spec.
