"""Runs `--revise` and checks the revision contracts (testing plan: T09-T12, Phase 2).

Calls Claude Code: runs only with --run-agent.
"""

import difflib
import re

import pytest

from conftest import (CASE_FOLDERS, CASE_IDS, FIXTURES, file_hashes, feature_number, load_expected,
                      new_project, parse_review, run_command)

pytestmark = pytest.mark.agent

NEW_FILES = {"epic-review.md", "spec.before-epic-revise.md", "epic-revise-log.md"}
QUANTITY = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:%|percent|ms|milliseconds?|seconds?|secs?|minutes?|mins?|hours?|days?|weeks?|"
    r"months?|years?|attempts?|times|tries|characters?|chars?|KB|MB|GB|requests?|items?)\b",
    re.I,
)
REQUIREMENT_LINE = re.compile(r"^\s*-\s*\*\*((?:FR|SC)-\d{3}[a-z]?)\*\*:?(.*)$", re.M)


# ---------- helpers ----------

def original_spec(folder):
    return (FIXTURES / folder / "spec.md").read_text(encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8")


def without_markers(text):
    return re.sub(r"\[NEEDS CLARIFICATION:[^\]]*\]", " ", text)


def invented_values(original, revised):
    known = {q.lower() for q in QUANTITY.findall(original)}
    return sorted({q.lower() for q in QUANTITY.findall(without_markers(revised))} - known)


def lost_ids(original, revised):
    ids = sorted(set(re.findall(r"\*\*((?:FR|SC)-\d{3})\*\*", original)))
    return [i for i in ids if not re.search(rf"\b{i}[a-z]?\b", revised)]


def applied_violations(log_text):
    """V-numbers the log lists as applied or needing a decision (everything before '## Skipped')."""
    body = log_text.split("## Skipped")[0]
    body = "\n".join(line for line in body.splitlines() if not line.startswith("**Selection"))
    return set(re.findall(r"\bV-\d{3}\b", body))


def requirement_lines(text):
    return {rid: line.strip() for rid, line in REQUIREMENT_LINE.findall(text)}


def changed_lines(a, b):
    return sum(1 for line in difflib.ndiff(a.splitlines(), b.splitlines()) if line[:2] in ("+ ", "- "))


# ---------- main run: <number> --revise high-only, once per fixture ----------

_runs = {}


@pytest.fixture
def revise_run(request, tmp_path_factory, extension_copy):
    folder = request.param
    if folder not in _runs:
        project, feature = new_project(request, tmp_path_factory, extension_copy, folder)
        before = file_hashes(feature)
        run_command(project, f"{feature_number(folder)} --revise high-only", case=request.node.callspec.id)
        _runs[folder] = {"feature": feature, "before": before, "after": file_hashes(feature)}
    return folder, _runs[folder]


def parametrize_cases(test):
    return pytest.mark.parametrize("revise_run", CASE_FOLDERS, ids=CASE_IDS, indirect=True)(test)


@parametrize_cases
def test_backup_and_log_are_created(revise_run):
    """T10: a revision log exists; if spec.md changed, the backup equals the original pre-revision spec."""
    folder, run = revise_run
    backup = run["feature"] / "spec.before-epic-revise.md"
    log = run["feature"] / "epic-revise-log.md"
    assert log.is_file() and log.stat().st_size > 0, "no revision log"
    if run["after"]["spec.md"] == run["before"]["spec.md"]:
        return  # nothing was applied, so there is nothing to back up
    assert backup.is_file(), "spec.md changed but there is no backup"
    assert backup.read_bytes() == (FIXTURES / folder / "spec.md").read_bytes(), "backup differs from the original"


@parametrize_cases
def test_only_spec_md_changes(revise_run):
    """T10: plan.md, tasks.md and other files stay unchanged; only the three expected files are new."""
    _, run = revise_run
    for path, digest in run["before"].items():
        if path != "spec.md":
            assert run["after"].get(path) == digest, f"revision changed {path}"
    new_files = set(run["after"]) - set(run["before"])
    assert new_files <= NEW_FILES, f"unexpected new files: {new_files - NEW_FILES}"


@parametrize_cases
def test_requirement_ids_are_kept(revise_run):
    """T09: original IDs are preserved, or split with letter suffixes (FR-004a, FR-004b)."""
    folder, run = revise_run
    lost = lost_ids(original_spec(folder), read(run["feature"] / "spec.md"))
    assert not lost, f"IDs missing after revision: {lost}"


@parametrize_cases
def test_no_invented_values(revise_run):
    """Revision does not invent values: every quantity outside clarification markers was in the original."""
    folder, run = revise_run
    invented = invented_values(original_spec(folder), read(run["feature"] / "spec.md"))
    assert not invented, f"values not in the original spec: {invented}"


@parametrize_cases
def test_unresolved_decisions_are_marked(revise_run):
    """Unresolved decisions are marked with [NEEDS CLARIFICATION: ...] instead of being guessed."""
    folder, run = revise_run
    forbidden = " ".join(load_expected(folder)["forbidden_revision_behaviors"]).lower()
    if "invent" not in forbidden and "without asking" not in forbidden:
        pytest.skip("this case has no decision the revision must leave open")
    assert "[NEEDS CLARIFICATION:" in read(run["feature"] / "spec.md")


@parametrize_cases
def test_high_only_applies_only_high_confidence(revise_run):
    """`--revise high-only` addresses only violations marked Confidence: high."""
    _, run = revise_run
    violations = parse_review(read(run["feature"] / "epic-review.md"))
    high = {v["id"] for v in violations if v["confidence"] == "high"}
    applied = applied_violations(read(run["feature"] / "epic-revise-log.md"))
    assert applied <= high, f"applied but not high confidence: {sorted(applied - high)}"


# ---------- single-case checks ----------

def one_case(case_id):
    return next(folder for cid, folder in zip(CASE_IDS, CASE_FOLDERS) if cid == case_id)


def test_selective_revision_changes_only_the_selected_violation(request, tmp_path_factory, extension_copy):
    """T11: `--revise V-001` addresses only V-001; requirements it does not name stay unchanged."""
    folder = one_case("T02")
    project, feature = new_project(request, tmp_path_factory, extension_copy, folder)
    run_command(project, f"{feature_number(folder)} --revise V-001", case="T11")
    applied = applied_violations(read(feature / "epic-revise-log.md"))
    assert applied == {"V-001"}, f"log lists {sorted(applied)}"
    v1 = next(v for v in parse_review(read(feature / "epic-review.md")) if v["id"] == "V-001")
    named = set(re.findall(r"\b(?:FR|SC)-\d{3}\b", v1["location"]))
    before, after = requirement_lines(original_spec(folder)), requirement_lines(read(feature / "spec.md"))
    changed = [rid for rid in before if rid not in named and after.get(rid) != before[rid]]
    assert not changed, f"V-001 is at {v1['location']!r}, but these also changed: {changed}"


def test_second_revision_pass_makes_fewer_edits(request, tmp_path_factory, extension_copy):
    """T12: a second `--revise high-only` pass avoids unnecessary additional edits."""
    folder = one_case("T01")
    project, feature = new_project(request, tmp_path_factory, extension_copy, folder)
    original = original_spec(folder)
    run_command(project, f"{feature_number(folder)} --revise high-only", case="T12")
    first = read(feature / "spec.md")
    run_command(project, f"{feature_number(folder)} --revise high-only", case="T12")
    second = read(feature / "spec.md")
    assert read(feature / "spec.before-epic-revise.md") == first, "backup of the second pass is not its input"
    assert not lost_ids(original, second), "IDs lost in the second pass"
    assert not invented_values(original, second), "values invented in the second pass"
    first_edits, second_edits = changed_lines(original, first), changed_lines(first, second)
    assert second_edits < first_edits, f"second pass changed {second_edits} lines, first pass {first_edits}"


def test_missing_feature_is_reported_without_changes(request, tmp_path_factory, extension_copy):
    """Invalid input: a feature number that does not exist writes nothing."""
    folder = one_case("T01")
    project, _ = new_project(request, tmp_path_factory, extension_copy, folder)
    before = file_hashes(project / "specs")
    run_command(project, "099 --revise", case="T01")
    assert file_hashes(project / "specs") == before, "files changed for a feature that does not exist"


def test_all_with_violation_numbers_is_refused(request, tmp_path_factory, extension_copy):
    """Invalid input: `--all --revise V-001` is refused (V-numbers differ per feature) and writes nothing."""
    folder = one_case("T01")
    project, _ = new_project(request, tmp_path_factory, extension_copy, folder)
    before = file_hashes(project / "specs")
    run_command(project, "--all --revise V-001", case="T01")
    assert file_hashes(project / "specs") == before, "files changed although the options are invalid"
