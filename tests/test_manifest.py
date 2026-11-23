"""Deterministic checks on the extension manifest, the command file and the references.

No AI agent is called. Run with: python -m pytest tests
"""

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "extension.yml"


@pytest.fixture(scope="module")
def manifest():
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def review_command():
    return (ROOT / "commands" / "speckit.epic-framework.review.md").read_text(encoding="utf-8")


def test_manifest_basic_fields(manifest):
    assert manifest["schema_version"] == "1.0"
    ext = manifest["extension"]
    assert ext["id"] == "epic-framework"
    assert re.fullmatch(r"\d+\.\d+\.\d+", ext["version"]), "version must be MAJOR.MINOR.PATCH"
    for key in ("name", "description", "author", "repository", "license"):
        assert ext.get(key), f"extension.{key} is missing"
    assert manifest["requires"]["speckit_version"].startswith(">=")


def test_manifest_commands_point_to_existing_files(manifest):
    commands = manifest["provides"]["commands"]
    assert commands, "at least one command is required"
    for cmd in commands:
        assert cmd["name"].startswith("speckit.epic-framework."), cmd["name"]
        assert (ROOT / cmd["file"]).is_file(), f"missing command file {cmd['file']}"
        assert cmd.get("description")


def test_only_the_review_command_is_provided(manifest):
    # The separate revise command was removed in v0.3.0.
    names = [c["name"] for c in manifest["provides"]["commands"]]
    assert names == ["speckit.epic-framework.review"]
    assert not (ROOT / "commands" / "speckit.epic-framework.revise.md").exists()


def test_command_file_has_frontmatter_description(review_command):
    match = re.match(r"^---\n(.*?)\n---\n", review_command, re.S)
    assert match, "command file must start with a --- frontmatter block"
    front = yaml.safe_load(match.group(1))
    assert front.get("description")


@pytest.mark.parametrize(
    "required_text",
    [
        "$ARGUMENTS",
        "--score",
        "--revise",
        "high-only",
        "--all",
        "epic-review.md",
        "spec.before-epic-revise.md",
        "epic-revise-log.md",
        "[NEEDS CLARIFICATION",
        "Never invent values",
        "Never renumber",
        "Want me to apply these fixes to spec.md?",
        ".specify/extensions/epic-framework/references/epic-skill.md",
        ".specify/extensions/epic-framework/references/practices.md",
    ],
)
def test_command_file_keeps_key_rules(review_command, required_text):
    assert required_text in review_command


def test_references_exist_and_cover_all_dimensions():
    skill = (ROOT / "references" / "epic-skill.md").read_text(encoding="utf-8")
    practices = (ROOT / "references" / "practices.md").read_text(encoding="utf-8")
    assert skill.strip() and practices.strip()
    for dim in ("E1", "E2", "E3", "P1", "P2", "I1", "I2", "I3", "C1", "C2"):
        assert f"### {dim} " in practices, f"practices.md has no section for {dim}"


def test_extensionignore_keeps_dev_files_out_of_installs():
    ignore = (ROOT / ".extensionignore").read_text(encoding="utf-8").splitlines()
    patterns = {line.strip() for line in ignore if line.strip() and not line.startswith("#")}
    assert {"tests/", ".github/"} <= patterns
    # Files the extension needs at runtime must not be ignored.
    for needed in ("commands/", "references/", "extension.yml", "LICENSE", "README.md"):
        assert needed not in patterns


def test_readme_documents_current_options():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for text in ("/speckit-epic-framework-review", "--revise", "--all", "--score"):
        assert text in readme
    assert "/speckit-epic-framework-revise" not in readme, "README still mentions the removed revise command"
