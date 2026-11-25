"""Runs the review (no --revise) on each fixture and checks it.

Calls Claude Code: runs only with --run-agent. One agent run per fixture.
"""

import re

import pytest

from conftest import (CASE_FOLDERS, CASE_IDS, FIXTURES, as_list, file_hashes, feature_number, load_expected,
                      matches_finding, new_project, normalize, parse_review, quoted_parts, run_command)

pytestmark = pytest.mark.agent

_runs = {}


@pytest.fixture
def review_run(request, tmp_path_factory, extension_copy):
    """Fresh project + fixture + review. Cached so the checks for one fixture share one agent run."""
    folder = request.param
    if folder not in _runs:
        project, feature = new_project(request, tmp_path_factory, extension_copy, folder)
        before = file_hashes(feature)
        run_command(project, feature_number(folder), case=request.node.callspec.id)
        report = feature / "epic-review.md"
        _runs[folder] = {
            "feature": feature, "before": before, "after": file_hashes(feature),
            "violations": parse_review(report.read_text(encoding="utf-8")) if report.is_file() else [],
        }
    return folder, _runs[folder]


def parametrize_cases(test):
    return pytest.mark.parametrize("review_run", CASE_FOLDERS, ids=CASE_IDS, indirect=True)(test)


# ---------- deterministic assertions ----------

@parametrize_cases
def test_review_writes_report_and_changes_nothing(review_run):
    """T08: review creates a nonempty epic-review.md and leaves spec.md byte-for-byte unchanged."""
    _, run = review_run
    report = run["feature"] / "epic-review.md"
    assert report.is_file() and report.stat().st_size > 0, "epic-review.md was not written"
    for path, digest in run["before"].items():
        assert run["after"].get(path) == digest, f"review changed {path}"
    new_files = set(run["after"]) - set(run["before"])
    assert new_files == {"epic-review.md"}, f"unexpected new files: {new_files - {'epic-review.md'}}"


@parametrize_cases
def test_findings_refer_to_existing_ids_and_quotes(review_run):
    """Report findings refer to existing requirement IDs and grounded quotes."""
    folder, run = review_run
    artifacts = "\n".join(p.read_text(encoding="utf-8") for p in (FIXTURES / folder).glob("*.md"))
    known_ids = set(re.findall(r"\b(?:FR|SC)-\d{3}[a-z]?\b", artifacts))
    artifact_text = normalize(artifacts)
    problems = []
    for v in run["violations"]:
        for rid in re.findall(r"\b(?:FR|SC)-\d{3}[a-z]?\b", v["location"]):
            if rid not in known_ids:
                problems.append(f"{v['id']}: {rid} does not exist")
        if any(name in v["location"] for name in ("spec.md", "plan.md", "tasks.md")):
            for part in quoted_parts(v["quote"]):
                if normalize(part) not in artifact_text:
                    problems.append(f"{v['id']}: quote not found in the artifacts: {part!r}")
    assert not problems, "\n  ".join(["ungrounded findings:"] + problems)


# ---------- semantic assertions (tolerant) ----------

@parametrize_cases
def test_review_finds_planted_problems(review_run):
    """The labeled EPIC issue was identified (requirement ID + dimension + evidence)."""
    folder, run = review_run
    missed = [f"{f['requirement_id']} {f['evidence']!r} ({'/'.join(as_list(f['dimension']))})"
              for f in load_expected(folder)["expected_findings"]
              if not any(matches_finding(v, f) for v in run["violations"])]
    assert not missed, "planted problems not found:\n  " + "\n  ".join(missed)


@parametrize_cases
def test_clean_specification_has_no_unsupported_findings(review_run):
    """T07: a well-specified feature (no expected findings) gets no high-confidence violations."""
    folder, run = review_run
    if load_expected(folder)["expected_findings"]:
        pytest.skip("not a clean specification")
    high = [f"{v['id']} {v['dimension']} {v['location']}" for v in run["violations"] if v["confidence"] == "high"]
    assert not high, "high-confidence findings on a clean specification:\n  " + "\n  ".join(high)
