---
name: epic-spec-quality
description: Review, score, write, or improve specification and planning artifacts for spec-driven development (SDD) with the EPIC framework (4 categories, 10 quality dimensions, 40 practices). Use whenever someone asks to assess, audit, critique, score, draft, or strengthen a spec.md, requirements.md, PRD, design.md, plan.md, tasks.md, constitution, OpenSpec proposal, or a Spec Kit or Kiro spec, or any document meant to guide an AI coding agent, even if EPIC is not mentioned.
---

# EPIC: quality of SDD specification and planning artifacts

In spec-driven development, the specification is what the coding agent acts on. A colleague who meets an ambiguous requirement asks a question; an agent usually resolves it on its own, plausibly and silently, and returns code that looks like an answer. EPIC describes the observable properties that make a set of specification and planning artifacts precise, consistent, and verifiable enough to guide AI-assisted implementation.

EPIC was derived from ISO/IEC/IEEE 29148:2018 and SDD tool guidance (Spec Kit, Kiro), populated with practices found in 114 open-source repositories that use SDD, checked against grey literature, and reviewed with practitioners. It has three levels:

- **4 categories**: the concern an agent faces (E Expressive, P Precise, I Interpretable, C Compartmentalized).
- **10 quality dimensions**: properties of the artifact set, each scored 0 to 3.
- **40 practices**: concrete ways of achieving a dimension (IDs such as E1.1).

| Category | Question it answers for the agent | Dimensions |
|---|---|---|
| **E** Expressive | What exactly is expected, and how will I know it is done? | E1 Unambiguous, E2 Singular, E3 Verifiable |
| **P** Precise | Under what conditions, and within what scope? | P1 Dependency Control, P2 Complete |
| **I** Interpretable | How do these files fit together? | I1 Conforming, I2 Consistent, I3 Comprehensible |
| **C** Compartmentalized | What must the product do, and what is the plan for building it? | C1 Scope Discipline, C2 Implementation-Planning Information |

## Pick the mode

- **Review**: the person shares existing artifacts and wants an assessment, a score, or feedback. Go to "Reviewing artifacts".
- **Author or revise**: the person wants a new spec set, or wants existing artifacts improved. Go to "Writing and revising artifacts".
- **Explain**: the person asks what a dimension or practice means. Answer from the practice list below, and read `references/practices.md` for full definitions and examples.

If the request is ambiguous (for example, "look at my spec"), review first and offer revisions at the end.

## Step 1: Gather the artifact set

EPIC assesses the artifacts **as a set**, because several dimensions (I2, I3, C1, C2) concern how files relate. Before judging anything, find and read every file that belongs to the feature or change:

| Workflow | Typical artifacts |
|---|---|
| Spec Kit | `spec.md`, `plan.md`, `tasks.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`, and the constitution under `.specify/memory/` |
| Kiro | `requirements.md`, `design.md`, `tasks.md` under `.kiro/specs/<feature>/`, plus steering files |
| OpenSpec | `proposal.md`, `design.md`, `tasks.md`, and spec deltas under `openspec/changes/<change>/`, plus `openspec/specs/` |
| No framework | `spec.md`, `requirements.md`, `PRD.md`, design docs, task lists, and agent instruction files (`AGENTS.md`, `CLAUDE.md`) that constrain implementation |

List the files you read in your answer. When a repository holds several features, assess one feature directory at a time unless the person asks for a repository-level view. If you only received part of the set (for example, a spec without its plan), say so, because a missing plan affects C2 and P1.

## Reviewing artifacts

### How to score

Score each of the ten dimensions from 0 to 3 using the rubric below. The total ranges from 0 to 30.

1. Read the whole set once before scoring, so that evidence found in `tasks.md` can count for a dimension you first looked for in `spec.md`.
2. For each dimension, look for its practices (listed below). Collect verbatim quotes with their file names as evidence.
3. Assign the level whose description fits the set as a whole. A level 3 means consistent evidence **throughout** the artifacts, so a single excellent section does not earn a 3 if the rest does not follow it.
4. Name the practices that are present, and the ones that are missing or weak.
5. Recommend the few changes that would raise the lowest scores, most important first.

Things that commonly distort a score:

- **Unfilled template text is not evidence.** Many repositories keep template placeholders such as `FR-001: System MUST [specific capability]` or a bare `[NEEDS CLARIFICATION]`. A filled template shows structure (I1), but placeholders left in a spec presented as final count against E1 and P2.5.
- **Length is not quality.** A short spec for a small feature can score 3. Judge whether each requirement is precise, singular, and checkable, not how much text exists.
- **Not every practice applies.** E2.5 (security and privacy properties) matters only when the feature handles sensitive data or exposes an attack surface. Do not lower a score for a practice that the feature has no reason to use, and say when you judged one not applicable.
- **Missing files count as missing evidence.** If there is no task breakdown anywhere, C2 cannot be high. Say whether the file is absent from the repository or only absent from what you were given.

### Rubric

| Dim. | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **E1 Unambiguous** | Pervasive vague terms ("user-friendly", "fast", "as appropriate") with no definitions. | Some requirements precise; many use unbounded or ambiguous terms. | Most requirements use measurable or bounded terms; key terms are defined (glossary, schema, or enumerations). | Every requirement has one interpretation; open questions are surfaced with markers or resolved in a clarifications record, not guessed. |
| **E2 Singular** | Many requirements bundle several capabilities ("support X and Y and Z"). | Some singular; many compound. | Most state a single capability, with occasional compounding. | Every requirement states exactly one capability, characteristic, constraint, or quality; compound "and/or" statements are absent or deliberately split. |
| **E3 Verifiable** | Largely unverifiable ("works well"); no acceptance criteria, scenarios, or measurable success criteria. | Some acceptance criteria or informal validation notes; many requirements remain hard to test. | Most functional requirements have measurable criteria linked to concrete checks (Given/When/Then, expected inputs and outputs, contract checks); edge and failure cases are uneven. | Every requirement is testable and mapped to verification evidence, including error handling and end-to-end user workflows; completion conditions are explicit. |
| **P1 Dependency Control** | No assumptions, dependencies, or constraints discussed. | Mentioned in passing, not systematically. | Assumptions, dependencies, and constraints documented at the artifact level (for example, dedicated sections). | Non-trivial requirements and tasks are paired with their dependencies and constraints; risks are traced to specific requirements; dependency checks and failure behavior are specified. |
| **P2 Complete** | Major content absent (no error handling, no non-functional requirements, no interfaces); many unresolved TBD items. | Happy path covered; invalid input, edge cases, and non-functional requirements largely missing. | Functional, performance, interface, and constraint content present where applicable; some TBD items remain. | All applicable content covered (stories, acceptance and success criteria, exceptional behavior, constraints, delivery); every open item is resolved or carries status and a resolution plan. |
| **I1 Conforming** | No template or style consistency; no requirement IDs. | Inconsistent style; some requirements have IDs. | Most requirements follow a consistent template; IDs present and stable, with gaps. | Every requirement follows an explicit, declared template and has a unique ID that is never changed or reused. |
| **I2 Consistent** | Visible contradictions in behavior, ordering, units, or terminology. | Same concept named differently across places; inconsistent units or notation. | Terminology and units largely consistent; no contradictions detected. | Standard terminology defined and used uniformly across all artifacts; units and notation homogeneous; no conflict between requirements or files. |
| **I3 Comprehensible** | Scattered, no entry point; documents duplicate or contradict each other without cross-references. | Most information findable with effort; no clear entry point; relationships between documents implicit. | Clear entry point; cross-references mostly present; relation to the parent context explained. | Entry point names the constituent documents; cross-references consistent in both directions; the set reads as a coherent whole, with aids (file purposes, legends, rationale, examples). |
| **C1 Scope Discipline** | Spec dominated by technology choices, code, architecture, schedules, or process. | User-facing requirements mixed with implementation prescriptions or project-management content. | Mostly behavioral and product-focused, with occasional leakage. | Strictly behavioral; design decisions, technical context, and tasks live in dedicated plan, design, or task artifacts that trace back to the requirements. |
| **C2 Implementation-Planning Information** | Nothing enabling implementation: no technical context, task breakdown, or contracts. | One of {technical context and rationale, task breakdown, data or API contracts} present but minimal. | Two of the three substantively present, with explicit links from requirements to plan items. | All three substantively present and linked to requirements in both directions; assumptions, dependencies, and phasing across versions addressed; governing principles (for example, a constitution) exist where architectural discipline matters. |

### Review output

Use this structure unless the person asks for something else:

```markdown
# EPIC review: <feature or change name>

**Artifacts reviewed:** <files>
**Total:** <n>/30 | E <n>/9 | P <n>/6 | I <n>/9 | C <n>/6

## Summary
<Two to four sentences: strongest dimensions, weakest dimensions, the most important risk for an agent implementing from this set.>

## Scores
| Dimension | Score | Practices present | Missing or weak |
|---|---|---|---|
| E1 Unambiguous | 2 | E1.2, E1.3 | E1.1 |
| ... | | | |

## Evidence and gaps
### E1 Unambiguous (2/3)
- Present, E1.2: "<verbatim quote>" (spec.md)
- Missing, E1.1: <what is absent and where it matters>
<Repeat for each dimension. Keep each to a few lines.>

## Recommended revisions
1. <Highest-impact change, the practice it applies (ID), and where to make it>
2. ...
```

When the person needs machine-readable output (for example, scoring many repositories), return JSON with this shape instead:

```json
{
  "artifacts": ["spec.md", "plan.md", "tasks.md"],
  "scores": {
    "E1": {"score": 2, "present": ["E1.2", "E1.3"], "missing": ["E1.1"], "not_applicable": [],
           "evidence": [{"practice": "E1.2", "file": "spec.md", "quote": "..."}],
           "rationale": "..."}
  },
  "total": 21
}
```

Include all ten dimensions (E1, E2, E3, P1, P2, I1, I2, I3, C1, C2) in `scores`.

## Writing and revising artifacts

When drafting, work from the outside in: decide where content belongs (C), then write each requirement well (E), then record what it depends on and covers (P), then make the set hang together (I).

**C (Compartmentalized): separate what from how.**
- Put externally observable behavior, user goals, and product constraints in the specification (C1.1). Put technology choices, architecture, data models, and tasks in plan, design, or task files (C1.2).
- Give the plan technical context, a phased task breakdown with dependencies and parallel markers, and data or API contracts (C2.1, C2.2, C2.4).
- Label every task with the requirement or story it serves, and link the plan back to the spec (C1.3, C2.3).

**E (Expressive): express one thing, one way.**
- Write one obligation per requirement, with one normative verb (MUST, SHALL, MUST NOT) used consistently (E2.1, E1.4).
- Replace vague qualities with thresholds, bounds, defaults, or enumerated values (E1.2, E1.3).
- Give each requirement or story acceptance criteria and a way to check it independently, including failure and edge cases (E3.1 to E3.3), and state when verification counts as complete (E3.4).
- State exclusions explicitly, with a reason ("does NOT ...", "deferred to v2 because ...") (E1.5).

**P (Precise): pinpoint dependencies and coverage.**
- Record assumptions, dependencies, target platform, and constraints in dedicated sections (P1.1, P1.2), and attach them to the requirements or tasks they affect (P1.3).
- Specify what happens when a dependency is missing or fails, and how it is verified (P1.4).
- Cover error handling, edge cases, and non-functional requirements, not only the happy path (P2.2, P2.3).
- Track open items with a status and a plan for resolving them (P2.5).

**I (Interpretable): make the set readable as a whole.**
- Follow the template of the workflow in use, and declare it (I1.1, I1.3). Give requirements, criteria, and tasks stable IDs (I1.2).
- Define key terms once and reuse them exactly across every file; keep IDs, priorities, and units in one notation (I2.1, I2.2).
- Keep facts that appear in several files identical (I2.3), and give the set an entry point with cross-references between documents (I3.1, I3.2).

Two behaviors matter most when an agent writes specifications:

- **Do not guess at decisions the person has not made.** If a threshold, scope boundary, or behavior is unknown, ask, or insert a clarification marker (for example, `[NEEDS CLARIFICATION: maximum file size?]`) and list the open questions at the end. An invented number reads as a requirement and will be implemented as one (E1.1, P2.5).
- **Respect the conventions already in use.** When revising, keep existing IDs (renumbering breaks I1.2 and every trace link), keep the workflow's template, and make the smallest change that applies the practice. After revising, list the changes with the practice IDs they apply.

## The 40 practices

Full definitions, signals, and examples from the analyzed repositories are in `references/practices.md`. Read the relevant section there when you need to decide whether a passage counts as evidence of a practice.

**E1 Unambiguous**
- E1.1 Explicit Clarification-Seeking: unresolved questions are surfaced (markers, clarifications record, guardrails for judgment calls), not silently resolved.
- E1.2 Quantified / Measurable Requirements: thresholds, time bounds, percentages, or exact outcomes.
- E1.3 Bounded Vocabulary & Enumerated Definitions: key terms, value domains, defaults, and states fixed by a glossary, enum, schema, or external standard.
- E1.4 Normative & Structural Consistency: one modal-verb convention, fixed reference templates, a named source of truth, explicit ordering.
- E1.5 Explicit Scope & Verification Boundaries: stated exclusions and deferrals with reasons, and how each requirement is checked independently.

**E2 Singular**
- E2.1 Atomic Functional & Behavioral Statements: one capability, story, task, or exclusion per statement.
- E2.2 Singular Architecture & Design Facts: one technical constraint, decision, property, or trade-off per entry.
- E2.3 Isolated Risk, Assumption, Edge-Case & Constraint Entries: each risk, mitigation, assumption, edge case, and constraint recorded separately.
- E2.4 Singular Definitional, Scenario & Relational Statements: one term per definition, one outcome per scenario, one relationship per dependency line, one measure per success criterion.
- E2.5 Singular Security & Privacy Properties: data captured, protection mechanism, and privacy implication stated separately.

**E3 Verifiable**
- E3.1 Verification Criteria & Measurable Outcomes: acceptance criteria, success metrics, and performance goals that decide whether a requirement is met.
- E3.2 Verification Scenarios & Validation Methods: Given/When/Then scenarios, executable checks, test references, validation procedures.
- E3.3 Comprehensive Verification Coverage: edge cases, invalid inputs, limits, failure conditions, and tests that must fail first.
- E3.4 Verification Completion & Readiness: gates and conditions for when verification is complete and work can be accepted.

**P1 Dependency Control**
- P1.1 Declared Assumptions & Dependencies: services, libraries, platforms, permissions, preconditions, and assumptions named in a dedicated place.
- P1.2 Explicit Constraint & Scope Boundaries: hard limits on resources, operation, domain, and integration, plus phase-level scope decisions.
- P1.3 Requirement/Task-Level Dependency & Risk Traceability: dependencies and risks attached to the specific requirement, task, or phase, with the reason for ordering.
- P1.4 Dependency Verification & Failure-Mode Handling: checks that prerequisites hold, and behavior when they do not.

**P2 Complete**
- P2.1 Functional and User Requirement Coverage: requirements, stories, workflows, acceptance and success criteria, and key entities.
- P2.2 Exceptional Behavior & Scope Definition: error handling, edge cases, risks with mitigations, and out-of-scope statements.
- P2.3 Technical, Operational & Quality Constraints: non-functional requirements, technical context, governance rules, decisions, and interfaces.
- P2.4 Dependency & Delivery Planning: sequencing, migrations, delivery scope, and capabilities deferred to later versions.
- P2.5 Specification Completeness Management: clarifications recorded, and open items tracked with status and a resolution path.

**I1 Conforming**
- I1.1 Standardized Document Structure: the same metadata block and named sections in the same order for every artifact of a type.
- I1.2 Stable, Unique Requirement Identifiers: IDs assigned once, never reused, with renames recorded.
- I1.3 Explicit Template Declaration & Enforcement: the template or schema named, the expected format shown, and a validation command or linter where possible.

**I2 Consistent**
- I2.1 Standardized Terminology & Concept Definitions: one vocabulary for concepts, states, and technologies, reused everywhere.
- I2.2 Uniform Identifiers & Notation: one convention for IDs, priorities, units, dates, and status.
- I2.3 Cross-Artifact Alignment & Traceability: the same facts, names, and fields stated identically in every file that uses them.
- I2.4 Consistent Organizational Structure: one structural pattern for stories, scenarios, and sections, with each concern in exactly one place.

**I3 Comprehensible**
- I3.1 Structured Document Organization: an entry point, a clear hierarchy, and dedicated sections.
- I3.2 Cross-Document Context & Navigation: sibling documents listed, cross-references, parent context, and next steps.
- I3.3 Comprehension Support: file-purpose notes, legends, examples, rationale, status markers, and orienting statements.

**C1 Scope Discipline**
- C1.1 Behavioral Product Specification: observable behavior, user goals, and product constraints, independent of technology.
- C1.2 Separation of Product & Project Concerns: design, technical context, plans, and tasks kept in dedicated artifacts.
- C1.3 Traceable Transition to Implementation: links from requirements to implementation work without moving implementation detail into the spec.

**C2 Implementation-Planning Information**
- C2.1 Technical Context & Implementation Foundations: technologies, environments, permissions, dependencies, and governing principles.
- C2.2 Implementation Planning & Task Organization: phases, task decomposition, ordering, and parallelization.
- C2.3 Requirements-to-Implementation Traceability: requirements linked to plans, tasks, validation, and decision records.
- C2.4 Implementation Data Models & Evolution Planning: data models, contracts, schemas, and allocation of functionality across releases.

## Limits to keep in mind

- Scores describe the artifacts, not the people who wrote them. Phrase feedback accordingly.
- In the study behind EPIC, repositories with higher scores tended to have less complex code, lower vulnerability density, and fewer bug-fix commits. These are associations, not guarantees; do not promise that raising a score will improve the code.
- Your scores are your own judgment. They have not been calibrated against the study's human raters, so always show the evidence behind each score and let the person disagree with it.
- Quote only text that appears in the artifacts. If you cannot find evidence for a practice, say it is missing; do not paraphrase something into existence.

