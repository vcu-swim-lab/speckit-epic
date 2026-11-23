"""Deterministic checks on the test fixtures (spec.md + expected.json).

They make sure every answer key is well formed and points at text that really exists in its spec.
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
    spec = (case_dir / "spec.md").read_text(encoding="utf-8")
    expected = json.loads((case_dir / "expected.json").read_text(encoding="utf-8"))
    return spec, expected


def test_there_are_fixtures():
    assert CASE_DIRS, "no fixture folders found"


@pytest.mark.parametrize("case_dir", CASE_DIRS, ids=lambda p: p.name)
def test_folder_layout(case_dir):
    assert re.match(r"^T\d{2}-[a-z0-9-]+$", case_dir.name), "folder must be named like T01-short-name"
    assert (case_dir / "spec.md").is_file()
    assert (case_dir / "expected.json").is_file()


@pytest.mark.parametrize("case_dir", CASE_DIRS, ids=lambda p: p.name)
def test_expected_json_schema(case_dir):
    _, expected = load(case_dir)
    assert expected["case_id"] == case_dir.name[:3]
    for key in ("title", "planted_problem", "forbidden_revision_behaviors", "expected_revision_behavior"):
        assert key in expected, f"missing key {key}"
    assert isinstance(expected["expected_findings"], list)
    assert isinstance(expected["forbidden_revision_behaviors"], list)
    if not expected["expected_findings"]:
        # A clean control must say what counts as a failure.
        assert expected.get("fail_if"), "a fixture with no expected findings needs a fail_if rule"
    for finding in expected["expected_findings"]:
        for key in ("location", "dimension", "evidence", "expected_issue"):
            assert key in finding, f"finding is missing {key}"
        assert set(as_list(finding["dimension"])) <= DIMENSIONS, finding["dimension"]


@pytest.mark.parametrize("case_dir", CASE_DIRS, ids=lambda p: p.name)
def test_evidence_and_locations_exist_in_spec(case_dir):
    spec, expected = load(case_dir)
    entries = expected["expected_findings"] + expected.get("must_not_flag", [])
    for entry in entries:
        for evidence in as_list(entry.get("evidence", [])):
            assert evidence in spec, f"evidence {evidence!r} is not in spec.md"
        for location in as_list(entry["location"]):
            if REQUIREMENT_ID.match(location):
                assert f"**{location}**" in spec, f"location {location} is not in spec.md"


@pytest.mark.parametrize("case_dir", CASE_DIRS, ids=lambda p: p.name)
def test_spec_follows_spec_kit_style(case_dir):
    spec, _ = load(case_dir)
    assert spec.startswith("# Feature Specification:")
    for section in ("## User Scenarios & Testing", "## Requirements", "## Success Criteria"):
        assert section in spec, f"missing section {section}"
    assert re.search(r"\*\*FR-\d{3}\*\*", spec), "no FR-### requirement found"
    assert " shall " not in spec.lower(), "use MUST (Spec Kit style), not shall"
    ids = re.findall(r"\*\*((?:FR|SC)-\d{3}[a-z]?)\*\*", spec)
    assert len(ids) == len(set(ids)), "duplicate requirement IDs"
