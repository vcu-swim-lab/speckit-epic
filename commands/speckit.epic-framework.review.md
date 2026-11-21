---
description: "Report the parts of the current feature's spec, plan, and tasks that violate EPIC practices, without fixing them"
---

# EPIC Review

Check the current feature's Spec Kit artifacts against the EPIC framework and write a report of the parts that **violate** EPIC practices. This command **only reports**. It never fixes, rewrites, or suggests replacement text.

## User Input

```text
$ARGUMENTS
```

The input is optional. It may contain:

- A feature directory (for example `specs/001-user-login`). If absent, use the current feature.
- `--score`: also include the 0–3 dimension scores. Without it, the report lists violations only.

## Reference material

The EPIC definitions live next to this command, in the installed extension:

- `.specify/extensions/epic-framework/references/epic-skill.md`: the EPIC categories, dimensions, rubric, and the 40 practices in short form.
- `.specify/extensions/epic-framework/references/practices.md`: full definitions, signals, and examples for each practice.

Read both before reviewing. Use them as the **only** source for what counts as a violation. Do not invent rules that are not in EPIC.

Ignore the "Writing and revising artifacts" section and the "Recommended revisions" part of the output template in `epic-skill.md`. This command does not revise.

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

## Guardrails

- **Never modify** `spec.md`, `plan.md`, `tasks.md`, or any other artifact. The only file this command writes is `FEATURE_DIR/epic-review.md`.
- **Never propose fixes**: no "Recommended revisions", no rewritten requirements, no suggested wording.
- **Never quote text that is not in the artifacts.**
- Phrase findings about the artifacts, not about the people who wrote them.

## Completion

Tell the user:

- The path to `epic-review.md`
- The number of violations per category (E, P, I, C)
- The three violations most likely to make an implementing agent guess, by V-number

Then ask:

> Want me to apply these fixes to spec.md? (yes / no / list of V-numbers / high-only)

- **No**: stop. Tell the user they can run the EPIC revise command later.
- **Yes**, a list of V-numbers, or `high-only`: run the EPIC revise command (`speckit.epic-framework.revise`) in this session the same way you would run any other command, passing the feature directory and the user's selection. Run it in the main session, not a sub-agent, so the user sees the diff.
- In automated or non-interactive mode, do not ask and do not revise.

Asking does not change the rule above: this command itself never modifies `spec.md`. Only the revise command does, and only after the user says yes.
