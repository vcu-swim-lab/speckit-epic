"""Installs this checkout into a fresh Spec Kit project and checks what lands there.

No AI agent is called. Skipped if the `specify` CLI is not installed.
"""

import re

import pytest

from conftest import ROOT, init_project


@pytest.fixture(scope="module")
def installed(tmp_path_factory, extension_copy):
    project = tmp_path_factory.mktemp("install") / "proj"
    init_project(project, extension_copy, ignore_agent_tools=True)
    return project


def test_extension_files_are_installed(installed):
    ext = installed / ".specify" / "extensions" / "epic-framework"
    for path in ("extension.yml", "LICENSE", "references/epic-skill.md", "references/practices.md"):
        assert (ext / path).is_file(), f"missing {path}"


def test_command_is_discoverable(installed):
    skill = installed / ".claude" / "skills" / "speckit-epic-framework-review" / "SKILL.md"
    assert skill.is_file()
    assert "--revise" in skill.read_text(encoding="utf-8")
    assert not (installed / ".claude" / "skills" / "speckit-epic-framework-revise").exists()


def test_development_files_are_not_installed(installed):
    ext = installed / ".specify" / "extensions" / "epic-framework"
    for path in ("tests", ".github", ".extensionignore", ".gitignore"):
        assert not (ext / path).exists(), f"{path} should not be installed (.extensionignore)"


def test_installed_version_matches_checkout(installed):
    def version(path):
        return re.search(r'^\s*version:\s*"?([^"\s]+)', path.read_text(encoding="utf-8"), re.M).group(1)

    installed_yml = installed / ".specify" / "extensions" / "epic-framework" / "extension.yml"
    assert version(installed_yml) == version(ROOT / "extension.yml")
