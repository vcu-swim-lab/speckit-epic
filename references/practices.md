# EPIC practices: definitions, signals, and examples

This file expands the 40 practices listed in `SKILL.md`. Each entry gives a definition, the signals that count as evidence, and short examples from specification artifacts analyzed in the EPIC study. Examples are excerpts, sometimes trimmed with "...", and file-level headings are separated with " / ". Use them to calibrate what a practice looks like in real artifacts, not as text to copy.

## Contents

- [E: Expressive](#e-expressive): E1 Unambiguous, E2 Singular, E3 Verifiable
- [P: Precise](#p-precise): P1 Dependency Control, P2 Complete
- [I: Interpretable](#i-interpretable): I1 Conforming, I2 Consistent, I3 Comprehensible
- [C: Compartmentalized](#c-compartmentalized): C1 Scope Discipline, C2 Implementation-Planning Information

## E: Expressive

When delegating work to an agent, a specification needs to communicate what the agent is expected to do and how its work will be assessed. Each requirement should have one intended interpretation (E1), express a single obligation (E2), and come with criteria for checking whether it has been met (E3).

### E1 Unambiguous

A requirement is stated so that it can be interpreted in only one way.

**E1.1 Explicit Clarification-Seeking.** Unresolved ambiguity is surfaced, not papered over. This takes three forms: inline markers at the exact point of uncertainty; a dedicated clarifications record where open questions are answered before the document is treated as final; and guardrails that pre-empt divergent readings of a borderline judgment call.

- Signals: `[NEEDS CLARIFICATION: ...]` markers with a specific question; a `## Clarifications` section with dated sessions or Q&A pairs; rules such as "when in doubt, do X and document what's left".
- Counter-signal: generic template markers left unfilled in a spec presented as final.
- Examples:
  - `## Clarifications ### Session 2026-01-13`
  - "When in doubt, leave it as 'In Progress' and document what's left."
  - "All NEEDS CLARIFICATION items resolved: ✅"

**E1.2 Quantified / Measurable Requirements.** Requirements and success criteria are stated as concrete, checkable facts (numeric thresholds, time bounds, percentages, or exact outcomes) instead of open-ended or subjective judgments.

- Signals: numbers with units and conditions; exact expected results for edge inputs.
- Examples:
  - "Operators can query any SuzieQ-supported network table and receive results within 5 seconds for networks up to 500 devices"
  - "SC-002: Roadmap page loads and renders all content within 3 seconds on a 3G connection"
  - "FR-024: System MUST handle division by zero in publication rate calculation by returning 0"

**E1.3 Bounded Vocabulary & Enumerated Definitions.** Key nouns, categories, value domains, defaults, and states have a single fixed referent. The meaning can be fixed internally (glossary, enum, schema), by drawing a status from a closed set of labels, or externally by pointing to an already-defined meaning (a standard, an error code).

- Signals: glossaries; enumerated values; explicit defaults and maxima; references to external definitions.
- Examples:
  - "FR-002: Container MUST default PUID to 1000 and PGID to 1000 when not specified"
  - "T056 [P] [US4] Test limit parameter (default 200, max 1000)"
  - "Storage: File-based (config.yaml input, README.md output, no database required)"

**E1.4 Normative & Structural Consistency.** The document uses one consistent way of expressing and locating requirements, so inconsistent presentation does not introduce ambiguity: uniform modal verbs, a fixed template for referencing files or task locations, a named single source of truth for each input, explicit sequencing of tasks or agents, and directives that placeholders must be removed before the spec counts as done.

- Examples:
  - "It MUST NOT touch the persistent 'MultiSweepService'/scheduled sweep config"
  - "Read the task file directly from .tasks/{subdirectory}/TASK-ID-name.md"
  - "Input: Feature specification from /specs/[###-feature-name]/spec.md"

**E1.5 Explicit Scope & Verification Boundaries.** The spec states what is and is not covered, with a reason, and how each requirement or story can be checked independently, so a reader does not assume the scope or the verification method.

- Examples:
  - "(persistent configuration) is deferred to a future enhancement."
  - "Tests: Not explicitly requested in the feature specification. Test tasks are omitted."
  - "Independent Test: Time a new developer from landing to first successful `wave run`"

### E2 Singular

Each requirement expresses one capability, characteristic, constraint, or quality, so it can be implemented, traced, and verified on its own.

**E2.1 Atomic Functional & Behavioral Statements.** Each user need, capability, task, or explicit exclusion is its own statement: one MUST, one user story, one checklist item, one "does NOT". At the document level, one concern per section or requirement block (for example, sub-lettered IDs such as FR-024a and FR-024b, or a rule such as "split if the description needs AND").

- Examples:
  - "FR-088: Audit records MUST be immutable (cannot edit or delete)"
  - "R7. Support max_depth parameter (default 8, max 15) to limit tree depth"
  - "This feature does NOT capture visual layout or screenshots."

**E2.2 Singular Architecture & Design Facts.** Each technical fact (a constraint, decision, property, purpose, or trade-off) is isolated as its own bullet or field. A trade-off stays singular by comparing one pair of options on one axis.

- Examples:
  - "All API calls via native `fetch` (Node 18+)"
  - "Text format vs JSON: Text is 3–5× more token-efficient but harder to parse programmatically."
  - "Single-file implementations until proven insufficient"

**E2.3 Isolated Risk, Assumption, Edge-Case & Constraint Entries.** Each risk, each mitigation, each assumption, each edge case, and each constraint is recorded as a separate entry, so it can be referenced, verified, or revisited on its own.

- Examples:
  - "Risk 2: UIDs not stable across snapshots." / "Mitigation: UIDs assigned in deterministic tree traversal order."
  - "UTC timezone is standard for all timestamps in the database"
  - "No real-time updates are required; eventual consistency is acceptable"

**E2.4 Singular Definitional, Scenario & Relational Statements.** Each Given/When/Then scenario resolves to one outcome, each glossary entry defines one term, each principle check evaluates one rule, each dependency line states one relationship, and each success criterion measures one thing.

- Examples:
  - "Artifact: Output file produced by a pipeline step"
  - "SC-001: Script completes execution in under 5 minutes for up to 10 sources"
  - "Attribute: A named property on a Kind with a type, optional constraints, and a value on each Node."

**E2.5 Singular Security & Privacy Properties.** Security- and privacy-relevant facts (what data is captured, what mechanism protects it, what privacy implication follows) are each stated as their own line, not blended into one general security paragraph. Applies when the feature handles sensitive data or exposes an attack surface.

- Examples:
  - "Data captured: Accessible names, ARIA attributes, element roles, CSS selectors."
  - "Redaction: Password and sensitive autocomplete fields replaced with [REDACTED]."
  - "Attack surface: Feature reads the DOM only."

### E3 Verifiable

The artifacts connect each expected outcome to the evidence used to decide whether it has been achieved.

**E3.1 Verification Criteria & Measurable Outcomes.** Explicit, objective criteria determine whether a requirement has been implemented: acceptance criteria, success metrics, quantitative thresholds, and performance goals. Includes pairing a named defect with the test that verifies its fix, and technical contracts stated precisely enough to check.

- Examples:
  - "Backend coverage ≥ 80% (from 54%)", together with a check command containing `fail-under=80`
  - "Performance Goals: Query results < 5s for < 1000 objects"
  - "SC-003: All configured sources are successfully processed in 90% of runs"

**E3.2 Verification Scenarios & Validation Methods.** Concrete procedures for checking requirements: functional scenarios, independent validation procedures, executable checks, references to test artifacts or quickstart steps, and validation against controlled environments or external systems.

- Examples:
  - "THEN validation fails with a cardinality error on `Library.parameter`"
  - "Local full gate: `bun validate full --profile ci --target wasm-gc`."
  - "T015 [US2] Test container startup without PUID/PGID and verify UID 1000:1000"

**E3.3 Comprehensive Verification Coverage.** Verification extends beyond normal behavior to edge cases, invalid inputs, limits, and failure conditions, including tests required to fail before the implementation exists.

- Examples:
  - "Scenario: Missing structured output fails the run"
  - "What happens when developers don't have Claude CLI installed?"
  - "Tests MUST be written and FAIL before implementation (TDD per Constitution)"

**E3.4 Verification Completion & Readiness.** Clear conditions for when verification is complete and a requirement counts as satisfied: completion criteria, gates that block completion, and tracked verification status.

- Examples:
  - "STOP and VALIDATE: Test User Story 1 independently"
  - "T045 Run `uv run pytest tests/unit/ctl/` to verify all unit tests pass"
  - "The lint `npm run check:conformance-citations` enforces both."

## P: Precise

To plan and carry out implementation work, an agent needs the conditions on which requirements depend and the scope the work is expected to address. This category connects explicit prerequisites and constraints (P1) with coverage of the intended requirements (P2).

### P1 Dependency Control

Assumptions, dependencies, and constraints that must hold for requirements to be realized are explicit and connected to the work they affect.

**P1.1 Declared Assumptions & Dependencies.** The spec names what its requirements rely on in a dedicated place (an Assumptions or Dependencies section, a Primary Dependencies or Target Platform field): external services and libraries, reference implementations, the runtime or platform, required permissions, preconditions, and assumptions about users or context.

- Examples:
  - "Target Platform: Linux containers (CUDA 12.9, Ubuntu 24.04 base)"
  - "Primary Dependencies: Commander.js 14, Zod 4, urql, gql.tada, chalk, ora"
  - "Users have appropriate permissions to run Docker containers"

**P1.2 Explicit Constraint & Scope Boundaries.** The spec states hard boundaries that shape what is feasible: resource or performance ceilings, restrictions on how the system may operate, limits on the functional domain, and rules for how components communicate. At the version level, it states that the current set is one phase of a larger roadmap, with specific capabilities deferred and a reason given.

- Examples:
  - "Constraints: Read-only operations only; no write/delete/configuration operations"
  - "Data MUST NOT be persisted by default."
  - "All code lives inside `office_os/` to stay compatible with `openenv push`."

**P1.3 Requirement/Task-Level Dependency & Risk Traceability.** Dependencies, constraints, and risks are attached to the specific requirement, task, or phase they affect, with the reason for the ordering, which places that information alongside the work.

- Examples:
  - "Dependencies: Task 1 (sequential - needs root to link properly)"
  - "Phase 3 (US2): Depends on Phase 1, can run parallel to US1"
  - "Legend: [P] = parallel-safe (distinct files, no ordering dependency)"

**P1.4 Dependency Verification & Failure-Mode Handling.** The spec specifies what happens at the edges of a dependency: a step confirming a prerequisite is satisfied before work proceeds, the behavior required when a dependency is unavailable or only partly met, the concrete files or modules a change depends on, and gates that prevent marking work complete while a dependency is unverified.

- Examples:
  - "Verify: `uv run --project office_os server` starts and `/health` returns OK"
  - "| API key not configured | Add escape route with setup link |"
  - "`npx mcp-swiss` works on Node.js 18, 20, 22"

### P2 Complete

The artifact set accounts for the requirements within the feature's stated scope, and makes remaining gaps visible.

**P2.1 Functional and User Requirement Coverage.** Intended behavior is described comprehensively from the user's perspective: functional requirements, user stories and workflows, acceptance and success criteria, key domain entities, and background on the current state that motivates the change.

- Examples:
  - "## Success Criteria *(mandatory)* ### Measurable Outcomes" followed by SC-001 through SC-010
  - "### Key Entities" listing Runtime User, Runtime Group, Critical Directories
  - "## 1. Overview / ### Context & Goals / ### Current Pain Points"

**P2.2 Exceptional Behavior & Scope Definition.** The limits of the system are documented: invalid conditions, error handling, edge cases, named risks paired with mitigations, and explicit out-of-scope statements.

- Examples:
  - "Scenario: Path does not exist ... THEN it SHALL return `{:error, "Path not found: <path>"}`"
  - An edge-case table pairing "Degenerate/near-zero triangles" with "Filter or robust epsilon"
  - "private owned-field debugging or introspection is out of scope for this change"

**P2.3 Technical, Operational & Quality Constraints.** The artifacts document the technical, operational, and quality information needed to characterize the system: non-functional requirements, technical context, assumptions and constraints, architectural principles and governance rules, recorded technical decisions, and interface or contract definitions.

- Examples:
  - "The system SHALL NOT shell out to the system `zip` command."
  - "## Constitution Check"
  - "The local-mode HTTP surface (`POST /hub/api`) remains for non-MCP clients."

**P2.4 Dependency & Delivery Planning.** The artifacts describe how the system will be delivered: sequencing, dependencies between parts, migrations, delivery scope and effort, capabilities deferred to later versions, and documentation deliverables.

- Examples:
  - "### Phase 5: Diagnostics & Tooling (0.5 day) / ### Phase 6: Tests & Benchmarks (0.5–1.0 day)"
  - "reserve the parameter but only support `url=` initially."
  - "File the MTR-onto-JetStream follow-up change/issue."

**P2.5 Specification Completeness Management.** Incomplete or evolving information is managed actively: clarifications and their resolutions are recorded, and outstanding items carry a status and a reference or plan for resolving them, distinguishing what is settled from what is not.

- Examples:
  - "> **Status: proposed (not yet implemented).** ... Do not archive until implemented."
  - "**Reference**: [league-mod#124](https://github.com/LeagueToolkit/league-mod/issues/124)"
  - "## Clarifications ### Session 2025-11-24"

## I: Interpretable

An agent working across specifications, plans, and task descriptions needs to understand how the information fits together. Recognizable conventions help it locate requirements (I1), compatible terminology preserves meaning across artifacts (I2), and contextual guidance explains how details relate to the intended product (I3).

### I1 Conforming

Artifacts adhere to an applicable template, schema, or set of document and identifier conventions.

**I1.1 Standardized Document Structure.** Every artifact of a given type follows the same layout: the same metadata block (branch, date, status, links) and the same named sections in the same order, so a reader who has seen one artifact knows where to find requirements, criteria, or governance checks in the next.

- Examples:
  - "Branch: 001-shell-reload-api | Date: 2026-03-08 | Spec: ./spec.md"
  - "## User Scenarios & Testing *(mandatory)*" / "## Requirements *(mandatory)*"
  - "## Why" / "## What Changes" / "## Impact"

**I1.2 Stable, Unique Requirement Identifiers.** Each requirement, task, or success criterion has an identifier that is assigned once and never reused or silently reassigned, even as wording or location changes. Renames and supersessions are recorded explicitly (a "renamed from/to" note, a redirect to the replacement).

- Examples:
  - "FR-001 ... FR-002 ... FR-012" and "SC-001 ... SC-002 ... SC-007"
  - "**Spec ID:** 000"
  - An OpenSpec "## RENAMED Requirements" section with FROM and TO entries

**I1.3 Explicit Template Declaration & Enforcement.** The artifact names the template or schema it follows, shows the expected format (ideally with a counter-example), offers a mechanical check (a validation command or linter), and explains deliberate departures from the template.

- Examples:
  - "schema: spec-driven"
  - "## Format: `[ID] [P?] [Story] Description`"
  - "`openspec validate [change-id] --strict`"

### I2 Consistent

Terms, identifiers, and statements agree within and across artifacts.

**I2.1 Standardized Terminology & Concept Definitions.** A common vocabulary is defined and reused: core concepts, lifecycle stages, architectural elements, domain terms, modal-verb strength, enumerated values, and the technology stack are named identically wherever they recur.

- Examples:
  - "Rename `Oa` → `OpenApi` across all affected classes and attributes."
  - "LinkSchema, RoadmapItemSchema, RoadmapCategorySchema, RoadmapSchema"
  - "Tech stack: Go, Terraform Plugin Framework"

**I2.2 Uniform Identifiers & Notation.** Identifiers, labels, units, priorities, timestamps, and status markers follow one format across all artifacts, including a single convention for completion state, placeholder values, and retired identifiers.

- Examples:
  - "(Priority: P1)" / "(Priority: P2)" / "(Priority: P3)"
  - Seven requirements using 35 SHALL and four SHALL NOT statements with no other modal variants, and each of 21 scenarios containing one GIVEN/WHEN/THEN triple
  - "T015 Verify responsive layout (mobile 320px, tablet 768px, desktop 1920px)"

**I2.3 Cross-Artifact Alignment & Traceability.** Requirements, constraints, filenames, references, and guidance stay synchronized across artifacts. Information repeated in several files says the same thing, reciprocal fields in linked tasks match, and shared conventions are cited identically.

- Examples:
  - The response fields `checks_completed` and `checks_skipped` used identically in the specification, its error cases, and the implementation plan
  - plan.md "Performance Goals: Complete execution in under 5 minutes for up to 10 sources" matching spec.md "SC-001: Script completes execution in under 5 minutes for up to 10 sources"
  - A limit stated in the spec reappearing unchanged in tasks.md: "T056 [P] [US4] Test limit parameter (default 200, max 1000)"

**I2.4 Consistent Organizational Structure.** Information is organized with the same structural conventions throughout the project: stories, priorities, scenarios, schemas, and sections follow one pattern, and each concern occupies exactly one place.

- Examples:
  - "User stories should be PRIORITIZED as user journeys ordered by importance."
  - "Scenario: Valid SQLView validates" / "Scenario: Wrong type rejected"
  - "## Complete / ## Rejected / ## Consolidated", separated by identical `---` rules throughout

### I3 Comprehensible

The artifact set provides the context and navigation needed to interpret individual requirements as parts of a coherent product.

**I3.1 Structured Document Organization.** A clear structure lets readers understand the hierarchy and locate information: an entry point, logical and hierarchical sections, dedicated sections for topics such as assumptions and scope, a metadata block establishing the document's identity, and guidance for choosing between alternative layouts.

- Examples:
  - "# Spec: mcp-swiss Project Overview" with "**Spec ID:** 000" and "**Status:** Implemented ✅"
  - "### High Priority / ### Medium Priority / ### Low Priority / ### Unprioritized"
  - A product requirements document organized into fifteen numbered sections, from the problem statement to non-goals

**I3.2 Cross-Document Context & Navigation.** The artifacts explain how documents relate to each other and to the wider project: the sibling documents in the set are listed, cross-references and prerequisite links are present, parent context is linked (tickets, prior versions, the existing system), and navigation points to next steps.

- Examples:
  - "Input: Design documents from `/specs/001-yaml-first-docs/`"
  - "## Next Steps / → `/workflows:plan` for implementation details"
  - "**Ticket**: [NCN-113655](https://jira.nutanix.com/browse/NCN-113655)"

**I3.3 Comprehension Support.** Supporting information reduces the effort needed to interpret the artifacts: file-purpose annotations, notation legends, worked examples, rationale for decisions, explicit status markers, definitions, authoring guidance in templates, and orienting statements about what the product is and is not.

- Examples:
  - "This is a prompt flow editor, not a chat app."
  - "├── plan.md # This file (/speckit.plan command output)"
  - "**Last Updated**: 2026-04-30 09:35 UTC / **Status**: READY TO START"

## C: Compartmentalized

An agent needs to distinguish what the product must do from the decisions and tasks involved in building it. This category connects a specification focused on intended behavior (C1) with supporting artifacts that guide implementation (C2).

### C1 Scope Discipline

Product specifications distinguish required behavior and product constraints from discretionary design choices and project-management content.

**C1.1 Behavioral Product Specification.** The product is described through externally observable behavior, user goals, and product constraints, independent of particular technologies or architectures. Technical information belongs here only when it is a necessary product constraint (a required compatibility, interface, or operating condition).

- Examples:
  - "As a network engineer, I want to query what the network looked like at a specific point in time"
  - "Every transform must be safe and produce a valid wasm module."
  - "AND the uncompressed directory is removed after successful compression"

**C1.2 Separation of Product & Project Concerns.** Design decisions, technical context, implementation plans, and tasks are kept in dedicated artifacts, so the specification stays focused on the product.

- Examples:
  - A plan that begins "Input: Feature specification from /specs/001-shell-reload-api/spec.md"
  - "# SelectBuilder OpenAPI Schema Assertions / Implementation Plan"
  - Design decisions, technology stacks, and task lists appearing only in plan and task artifacts

**C1.3 Traceable Transition to Implementation.** Behavioral requirements are explicitly linked to the implementation work that realizes them, without moving implementation details into the specification itself.

- Examples:
  - "[Story] labels ensure traceability to requirements in spec.md"
  - "FR-002 → Task 2 (Detect) + Task 3 (Open dispatch)."
  - "Organization: Tasks grouped by user story for independent implementation."

### C2 Implementation-Planning Information

Supporting plan and task artifacts record how the work will be implemented.

**C2.1 Technical Context & Implementation Foundations.** The technical context needed for implementation: technologies, execution environments, permissions, operational assumptions, dependencies and how they are verified, architectural constraints, governance principles, and implementation-relevant domain concepts.

- Examples:
  - "Serialize `moon` commands because they contend on `_build/.moon-lock`."
  - "Verify Docker build: `docker build -t office_os-env:latest -f server/Dockerfile .`"
  - "Per [RFC 9110 Section 4.3.4 (PUT)](https://httpwg.org/specs/rfc9110.html#PUT)"

**C2.2 Implementation Planning & Task Organization.** A structured implementation strategy: plans, project structure, phases, task decomposition, dependencies, execution order, and opportunities for parallel work.

- Examples:
  - "## Phase 2: Foundational (Blocking Prerequisites)"
  - "[P]: Can run in parallel (different files, no dependencies)"
  - "├── contracts/ # Phase 1 output (API specifications)"

**C2.3 Requirements-to-Implementation Traceability.** Requirements are connected to plans, tasks, validation activities, and the documents that govern implementation choices (decision records, external specifications), so each requirement can be followed to its realization.

- Examples:
  - "FR-001 → Task 8 (skeleton), Task 9 (validation), Task 10 (run)."
  - "**Full Decision Details**: See `docs/testing/PUT_SEMANTICS_DECISION.md`"
  - "Input: Feature specification from /specs/001-suzieq-mcp-server/spec.md"

**C2.4 Implementation Data Models & Evolution Planning.** Structured information about data concepts, interfaces, and contracts (preliminary data models, entity relationships, schemas, API contracts, status or version fields) and about how functionality is distributed across releases.

- Examples:
  - "interface ExtractedLink { url: string; text: string; // Anchor text context: string; ... }"
  - "contracts/ └── shell-reload-api.yaml"
  - "Additional optional features (carousel, advanced OG generation) deferred to future scope."
