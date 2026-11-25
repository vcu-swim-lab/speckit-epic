"""Checks the fixture schemas and labels (testing plan, section 5, Tier A).

Every fixture folder has spec.md + expected.json, and every label points at text that exists.
No AI agent is called. Run with: python -m pytest tests
"""

import json
import re
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CASE_DIRS = sorted(p for p in FIXTURES.iterdir() if p.is_dir())
DIMENSIONS = {"E1", "E2", "E3", "P1", "P2", "I1", "I2", "I3", "C1", "C2"}
REQUIREMENT_ID = re.compile(r"^(FR|SC)-\d{3}$")


def as_list(value):
    return value if isinstance(value, list) else [value]


def load(case_dir):
    return json.loads((case_dir / "expected.json").read_text(encoding="utf-8"))


def all_artifact_text(case_dir):
    """spec.md plus any other artifacts in the fixture (plan.md, tasks.md, ...)."""
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(case_dir.glob("*.md")))


def test_there_are_fixtures():
    assert CASE_DIRS, "no fixture folders found"


def test_case_ids_are_unique():
    ids = [load(d)["case_id"] for d in CASE_DIRS]
    assert len(ids) == len(set(ids)), ids


@pytest.mark.parametrize("case_dir", CASE_DIRS, ids=lambda p: p.name)
def test_folder_layout(case_dir):
    assert re.match(r"^[a-z0-9-]+$", case_dir.name), "folder must be named like ambiguous-response-time"
    assert (case_dir / "spec.md").is_file()
    assert (case_dir / "expected.json").is_file()


@pytest.mark.parametrize("case_dir", CASE_DIRS, ids=lambda p: p.name)
def test_expected_json_schema(case_dir):
    expected = load(case_dir)
    assert re.fullmatch(r"T\d{2}", expected["case_id"])
    assert isinstance(expected["expected_findings"], list)
    assert isinstance(expected["forbidden_revision_behaviors"], list)
    for finding in expected["expected_findings"]:
        for key in ("requirement_id", "dimension", "evidence", "expected_issue"):
            assert key in finding, f"finding is missing {key}"
        assert set(as_list(finding["dimension"])) <= DIMENSIONS, finding["dimension"]


@pytest.mark.parametrize("case_dir", CASE_DIRS, ids=lambda p: p.name)
def test_labels_point_at_existing_text(case_dir):
    spec = (case_dir / "spec.md").read_text(encoding="utf-8")
    artifacts = all_artifact_text(case_dir)
    file_names = {p.name for p in case_dir.glob("*.md")}  # for missing content, the evidence can be the file
    for finding in load(case_dir)["expected_findings"]:
        for evidence in as_list(finding["evidence"]):
            assert evidence in artifacts or evidence in file_names, \
                f"evidence {evidence!r} is not in any artifact of the fixture"
        for requirement_id in as_list(finding["requirement_id"]):
            if REQUIREMENT_ID.match(requirement_id):
                assert f"**{requirement_id}**" in spec, f"{requirement_id} is not in spec.md"
