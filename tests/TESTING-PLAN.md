# Testing plan for the `speckit-epic` extension

**Audience:** Developer/maintainer of [vcu-swim-lab/speckit-epic](https://github.com/vcu-swim-lab/speckit-epic)  
**Goal:** Add automated regression tests and a repeatable evaluation benchmark for the extension's EPIC reviews and revisions.  
**Recommendation:** Keep the initial test suite **inside the extension repository**. Run end-to-end tests in **temporary Spec Kit projects**, outside the extension source tree.

## 1. What the extension currently does

The README documents one agent command (since v0.3.0; the separate revise command was removed):

- `/speckit-epic-framework-review [feature-path] [--score] [--revise [high-only | violation-IDs]]` reviews feature artifacts and writes `epic-review.md` without changing the specification. It then asks whether to apply fixes; on "yes", or immediately with `--revise`, it revises `spec.md`, creates `spec.before-epic-revise.md`, and writes `epic-revise-log.md`.

Important behavioral contracts to test:

- Reviews identify EPIC practice IDs, locations, quotes, reasons, and confidence levels.
- Review-only execution leaves the original `spec.md` unchanged.
- Revision does not invent unspecified requirements or values; it marks unresolved decisions with `[NEEDS CLARIFICATION: ...]`.
- Revision preserves requirement IDs; a split compound requirement uses sub-letters (such as `FR-004a`, `FR-004b`).
- Revision changes only `spec.md` among existing project artifacts; it does not modify code, `plan.md`, `tasks.md`, checklists, or the constitution.
- Selective revision changes only the selected violations, and `--revise high-only` respects the confidence filtering.
- Without `--revise`, a non-interactive run writes the report and changes nothing else.

Treat these as documented *expected behaviors*, not as behaviors already validated by tests.

## 2. Keep tests in this repository

Advantages: tests change in the same PR as command instructions and EPIC rubric updates; CI can run automatically; unpublished changes are easy to test; less maintenance than a separate testing repository.

Consider a **separate benchmark repository later** only if the research expands to comparisons of multiple extension implementations, coding agents, or models, or if you need a frozen, independently versioned public evaluation dataset.

Suggested layout:

```text
speckit-epic/
├── commands/
├── references/
├── extension.yml
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── ambiguous-response-time/
│   │   │   ├── spec.md
│   │   │   └── expected.json
│   │   ├── compound-requirement/
│   │   ├── conflicting-requirements/
│   │   ├── missing-acceptance-criteria/
│   │   ├── missing-decision/
│   │   └── clean-specification/
│   ├── test_manifest.py
│   ├── test_installation.py
│   ├── test_review.py
│   └── test_revision.py
├── benchmarks/
│   ├── cases/
│   ├── labels.jsonl
│   ├── run_benchmark.py
│   ├── score.py
│   └── README.md
└── .github/workflows/
    └── tests.yml
```

The exact layout may be adjusted to match existing repository conventions. Do not commit generated Spec Kit projects, generated reviews, API keys, or benchmark run outputs unless deliberately publishing a dataset.

## 3. Create a small fixture dataset

Start with **10–20 short specifications**, each containing one or two intentionally introduced problems. Add more realistic, longer examples later. Include *negative controls* (well-written requirements) to detect false positives. Cover the extension's ten documented EPIC dimensions:

- **Expressive:** E1 Unambiguous, E2 Singular, E3 Verifiable.
- **Precise:** P1 Dependency Control, P2 Complete.
- **Interpretable:** I1 Conforming, I2 Consistent, I3 Comprehensible.
- **Compartmentalized:** C1 Scope Discipline, C2 Implementation-Planning Information.

Suggested first test cases:

| ID | Fixture | Expected check |
|---|---|---|
| T01 | `FR-001: Users shall be able to log in quickly.` | Ambiguity / untestable performance term reported |
| T02 | One requirement combines validation and error display | Singular requirement issue identified |
| T03 | Requirement missing measurable acceptance criteria | Verifiability issue reported |
| T04 | Two requirements contradict each other | Inconsistency reported |
| T05 | Dependency on an undefined external service | Missing dependency information reported |
| T06 | Password reset link has no expiration policy | Missing decision flagged; no fabricated timeout |
| T07 | Well-specified feature | Avoid unsupported findings |
| T08 | Review operation | `spec.md` remains byte-for-byte unchanged |
| T09 | Revise compound requirement | Original ID preserved or split into letter-suffixed IDs |
| T10 | Revision operation | Backup and revision log created; unrelated files unchanged |
| T11 | Selective revision | Only requested violation IDs addressed |
| T12 | Second revision pass | Avoid unnecessary additional edits (idempotence expectation) |

Example fixture input (`tests/fixtures/ambiguous-response-time/spec.md`):

```markdown
# Feature: User Login

## Requirements

FR-001: Users shall be able to log in quickly.

FR-002: The system shall provide a secure and user-friendly authentication experience.

FR-003: Users shall be able to reset their password using an email link.

FR-004: The system shall validate credentials and display an error message on failure.
```

Example expected labels (`expected.json`):

```json
{
  "case_id": "T01",
  "expected_findings": [
    {
      "requirement_id": "FR-001",
      "dimension": "E1",
      "evidence": "quickly",
      "expected_issue": "ambiguous performance requirement"
    }
  ],
  "forbidden_revision_behaviors": [
    "inventing a numeric login time without a source"
  ]
}
```

**Important:** Have a person validate gold labels against the EPIC rubric before using them as ground truth. Some requirements can implicate more than one EPIC dimension. Record acceptable alternatives, and do not make tests depend on one exact wording.

## 4. Build isolated integration tests

For each fixture:

1. Create a fresh temporary directory (`pytest`'s `tmp_path` is appropriate).
2. Initialize or copy a minimal **valid Spec Kit project** into it.
3. Install the **local development checkout** of the extension, not the released ZIP, so the test exercises the code in the PR. The README documents `specify extension add --dev path/to/speckit-epic-main`; verify the exact CLI syntax in the installed Spec Kit version.
4. Copy the fixture into the feature's `specs/<feature>/spec.md`.
5. Invoke the agent through a scripted, non-interactive interface (for example, Claude Code `claude -p`, after confirming the installed CLI's options and permission settings). Ensure the prompt invokes the actual installed review/revise command; do not assume a textual request automatically routes to the intended command.
6. Capture exit status, stdout/stderr, agent logs when available, final artifacts, duration, and token/cost metadata if available.
7. Assert output contracts. Delete the temporary project at the end of the test, preserving it only when debugging failures.

Start with one manually verified run before automating. **Do not assume an agent CLI invocation is equivalent to a deterministic function call.** Set explicit file and command permissions in the test environment; do not use broad permissions or expose secrets to untrusted PRs.

### Deterministic assertions (should be strict)

- Extension manifest and command files exist and can be installed.
- Agent commands are discoverable in the initialized project.
- Review creates a nonempty `epic-review.md` and does not modify `spec.md`.
- Revision creates `spec.before-epic-revise.md` and `epic-revise-log.md`.
- Backup equals the original pre-revision spec.
- Review and revision leave unrelated project files untouched.
- Revision retains expected requirement IDs and records required human clarification.
- Report findings refer to existing requirement IDs / grounded quotes wherever the report format supports this validation.

### Semantic assertions (use more tolerant evaluation)

- The appropriate EPIC issue was identified, even when phrased differently.
- The revision improves the problem without changing intended behavior.
- The tool does not generate unjustified findings or invent missing values.
- Repeated runs produce sufficiently stable findings and revisions.

Use a small normalizer or structured parser to extract finding fields from `epic-review.md`. Prefer matching requirement ID + EPIC practice/dimension + evidence over exact prose strings. If using an LLM as a grader, manually audit a sample and distinguish grader error from extension error.

## 5. Separate CI tests from paid AI evaluations

**Tier A: quick PR checks** (default GitHub Actions job):

- Validate `extension.yml` and command/reference file structure.
- Run cheap scripts and parsers with pytest.
- Check fixture schemas and labels.
- Optionally run a local extension installation smoke test if it does not require a paid agent call.

**Tier B: agent-driven integration tests** (manual workflow dispatch, trusted branch, or protected release job):

- Test actual review and revision with one or two fixtures.
- Validate file contracts, installation behavior, and a few known findings.
- Apply timeouts and explicit spending limits; never expose API secrets to workflows from untrusted forks.

**Tier C: benchmark evaluation** (manually triggered / periodic when justified):

- Run all labeled examples multiple times using a recorded model, agent version, Spec Kit version, and extension commit.
- Save per-run findings, diffs, logs, model settings, and cost information.
- Compute evaluation scores and compare against the previous version.

Avoid gating every PR on noisy, expensive semantic LLM assertions until the dataset and scoring method have been validated.

## 6. Measure quality, not only execution success

For reviews:

- **Precision:** correctly reported violations divided by all reported violations.
- **Recall:** known violations found divided by all labeled violations.
- **False-positive rate:** unsupported findings on clean examples.
- **Coverage by EPIC dimension:** which categories are easy or hard.

For revisions:

- **Fix success:** fraction of targeted violations adequately resolved.
- **Regression rate:** fraction of revisions introducing new problems.
- **Intent preservation:** human or calibrated evaluator verifies no unauthorized semantic changes.
- **Clarification behavior:** unanswered product decisions remain explicitly flagged rather than guessed.
- **ID/file preservation:** deterministic checks on stable identifiers and unaffected artifacts.

For reliability and efficiency:

- **Run-to-run stability:** run each benchmark case about three times initially.
- **Latency, tokens, cost:** record when supported by the agent CLI.
- **Version comparison:** report regressions and improvements between extension commits.

Report overall results **and per-dimension results**. Label benchmark versions and publish the exact run configuration so comparisons are reproducible.

## 7. Reference implementation to inspect

**[artursopelnik/spec-kit-design-system](https://github.com/artursopelnik/spec-kit-design-system)** is an existing Spec Kit extension with:

- [`tests/`](https://github.com/artursopelnik/spec-kit-design-system/tree/main/tests): pytest suite.
- [`examples/`](https://github.com/artursopelnik/spec-kit-design-system/tree/main/examples): fixture/demo projects.
- [`benchmarks/`](https://github.com/artursopelnik/spec-kit-design-system/tree/main/benchmarks): cases, scorer, and benchmark reporting.
- [`.github/workflows/`](https://github.com/artursopelnik/spec-kit-design-system/tree/main/.github/workflows): CI. Its README describes an actual installation test and end-to-end example.

Use it for **test organization and installation smoke-test design**, not as a copy-paste solution: its purpose and command behavior differ from EPIC. Its README explicitly says the benchmark harness exists but published benchmark results are not yet available.

## 8. Implementation checklist, in order

### Phase 1 — Foundation

- [ ] Add `tests/` and pytest configuration/dependencies.
- [ ] Add 10–20 compact, labeled fixture specs covering all ten EPIC dimensions, including clean examples.
- [ ] Validate and version the gold labels.
- [ ] Add deterministic checks for manifest, command files, fixture schemas, and stable artifact naming.
- [ ] Configure a fast GitHub Actions PR workflow.

### Phase 2 — Real installation and workflow

- [ ] Add helper to create a temporary Spec Kit project and install the checked-out extension locally.
- [ ] Verify the review command creates the expected report without touching source specs.
- [ ] Verify the revision command creates a backup and log, preserves IDs, and leaves unrelated files unchanged.
- [ ] Test selective revision and `--revise high-only` behavior.
- [ ] Test unresolved decisions, repeat revision, and invalid or missing review inputs.
- [ ] Add a manually triggered, credential-protected agent integration workflow.

### Phase 3 — Empirical quality evaluation

- [ ] Write a finding extractor and matching/scoring script.
- [ ] Compare agent findings with labeled expected EPIC violations.
- [ ] Evaluate revised specs for fixes, invented requirements, and new regressions.
- [ ] Run cases repeatedly with fixed, documented settings.
- [ ] Publish a simple machine-readable CSV/JSON summary and a human-readable report.
- [ ] Add realistic multi-issue specifications after the small fixtures work.

### Definition of done for initial implementation

A maintainer can clone the repository, run a fast `pytest` command locally, run PR checks without API credentials, and optionally trigger an isolated real-agent test that generates a report, revises a fixture, and verifies the documented file and behavior contracts. Benchmark cases and their labels are versioned, and benchmark results can be reproduced with the recorded run settings.

## 9. Practical cautions

- Pin or record versions: Spec Kit, Claude Code/agent CLI, model, and extension commit. The extension README currently states Spec Kit 1.4.0+ and notes testing with 1.4.4 and Claude Code.
- LLM findings are judgments; a literal string mismatch is not necessarily a failure.
- Keep original fixture text immutable and avoid test-order dependencies.
- Keep generated outputs and secrets out of git unless explicitly published.
- Respect API quotas and test spending limits.
- Use the README's actual command syntax and output file names; verify CLI flags against the locally installed versions.
- Run integration tests inside disposable directories, never against the extension developer's working project.

## Sources

- EPIC extension repository and README: https://github.com/vcu-swim-lab/speckit-epic
- Example extension and README: https://github.com/artursopelnik/spec-kit-design-system
- Example extension tests: https://github.com/artursopelnik/spec-kit-design-system/tree/main/tests
- Example extension benchmarks: https://github.com/artursopelnik/spec-kit-design-system/tree/main/benchmarks
- Example extension CI: https://github.com/artursopelnik/spec-kit-design-system/tree/main/.github/workflows
