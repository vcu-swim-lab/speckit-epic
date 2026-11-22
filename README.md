# speckit-epic

A [GitHub Spec Kit](https://github.com/github/spec-kit) extension that checks your specifications against the [EPIC framework](https://epicframework.netlify.app/) for spec quality, reports what violates it, and can revise the spec for you.

## Why

In spec-driven development, a coding agent builds from the spec. When a requirement is vague ("log in quickly"), a human developer asks a question; an agent usually picks an answer silently and moves on. EPIC describes what makes a spec precise enough to build from. This extension brings that check into the Spec Kit workflow, before any code is written.

EPIC groups 40 practices into 10 quality dimensions and 4 categories:

| Category | Dimensions |
|---|---|
| **E**xpressive | E1 Unambiguous, E2 Singular, E3 Verifiable |
| **P**recise | P1 Dependency Control, P2 Complete |
| **I**nterpretable | I1 Conforming, I2 Consistent, I3 Comprehensible |
| **C**ompartmentalized | C1 Scope Discipline, C2 Implementation-Planning Information |

## Requirements

- [Spec Kit](https://github.com/github/spec-kit) 1.4.0 or later (tested with 1.4.4)
- A Spec Kit project (`specify init`)
- A coding agent supported by Spec Kit (tested with Claude Code)

## Install

From inside your Spec Kit project:

```
specify extension add --from https://github.com/vcu-swim-lab/speckit-epic/archive/refs/heads/main.zip
```

Spec Kit asks you to confirm installing from a URL. Answer `y`.

Or, in a new project:

```
specify init my-project --integration claude --extension https://github.com/vcu-swim-lab/speckit-epic/archive/refs/heads/main.zip --trust-extension-urls
```

Restart your agent session afterwards so it picks up the new command.

If the download fails (for example with an SSL certificate error), download the ZIP from GitHub in your browser (**Code → Download ZIP**), unzip it, and install from the folder:

```
specify extension add --dev path/to/speckit-epic-main
```

## Command

`/speckit-epic-framework-review` checks the current feature's artifacts against EPIC and writes `epic-review.md`. The report never proposes fixes. At the end it asks:

> Want me to apply these fixes to spec.md? (yes / no / list of V-numbers / high-only)

If you answer yes, it revises `spec.md` and shows what changed. With `--revise`, it skips the question and applies the fixes right away.

Options:

```
/speckit-epic-framework-review                        # current feature, then asks
/speckit-epic-framework-review specs/001-user-login   # a specific feature
/speckit-epic-framework-review --score                # also include 0-3 scores per dimension
/speckit-epic-framework-review --revise               # apply all fixes without asking
/speckit-epic-framework-review --revise high-only     # apply only high-confidence fixes
/speckit-epic-framework-review --revise V-001 V-020   # apply only these
```

## Workflow

```
/speckit-specify ──► spec.md
        │
        ▼
/speckit-epic-framework-review ──► epic-review.md
        │
  "Apply these fixes to spec.md?"  (skipped with --revise)
   │            │
   no          yes
   │            ▼
   │   revised spec.md + diff
   │            │
   │            ▼
   │   /speckit-clarify ──► you answer the open questions
   │            │
   │            └──► run /speckit-epic-framework-review again
   ▼
/speckit-plan ──► /speckit-tasks ──► /speckit-implement
```

`/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks` and `/speckit-implement` are Spec Kit's built-in commands.

## Files produced

All in the feature folder, for example `specs/001-user-login/`:

| File | Produced by | Contents |
|---|---|---|
| `epic-review.md` | always | Each violation with its EPIC practice ID, location, exact quote, reason and confidence |
| `spec.md` | after yes / `--revise` | The revised specification |
| `spec.before-epic-revise.md` | after yes / `--revise` | Backup of the spec before revision. Copy it back over `spec.md` to undo. |
| `epic-revise-log.md` | after yes / `--revise` | Which violations were fixed, which need a human decision, and which were skipped |

## How the revise step behaves

- **It never invents values.** If a fix needs a decision (for example, how long a reset link stays valid), it inserts `[NEEDS CLARIFICATION: ...]` instead. Answer these with `/speckit-clarify`.
- **It keeps requirement IDs.** Compound requirements are split with sub-letters (`FR-004` becomes `FR-004a`, `FR-004b`), never renumbered.
- **It changes only `spec.md`.** Code, `plan.md`, `tasks.md`, checklists and the constitution are left alone.

## Notes

- Findings are judgments made by an AI agent following the EPIC rubric. They are not calibrated against human raters, so check the quotes in the report.
- The EPIC rubric and practice definitions are in [`references/`](references/).

## License

[MIT](LICENSE). © 2026 Virginia Commonwealth University (VCU SE Center).
