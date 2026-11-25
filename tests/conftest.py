"""Shared helpers for the tests.

Free tests (no AI) always run:            python -m pytest tests
Agent tests call Claude Code and cost money. They run only when asked:
                                           python -m pytest tests --run-agent
Run one case only:                         python -m pytest tests --run-agent -k T01
Keep the temporary projects for debugging: add --keep-projects
"""

import hashlib
import json
import platform
import re
import shutil
import subprocess
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"

ALLOWED_TOOLS = (
    "Read,Glob,Grep,Write,Edit,Agent,Task,"
    "Bash(git diff:*),Bash(cp:*),PowerShell(Copy-Item:*),PowerShell(git diff:*)"
)
AGENT_TIMEOUT_SECONDS = 1200


def load_expected(folder):
    return json.loads((FIXTURES / folder / "expected.json").read_text(encoding="utf-8"))


# Each case: pytest id = case_id (T01), value = fixture folder name.
CASES = sorted((load_expected(p.name)["case_id"], p.name) for p in FIXTURES.iterdir() if p.is_dir())
CASE_FOLDERS = [folder for _, folder in CASES]
CASE_IDS = [case_id for case_id, _ in CASES]


def case_id_of(folder):
    return load_expected(folder)["case_id"]


def feature_number(folder):
    """T01 -> 001"""
    return "0" + case_id_of(folder)[1:]


def feature_dir_name(folder):
    """ambiguous-response-time -> 001-ambiguous-response-time"""
    return f"{feature_number(folder)}-{folder}"


# ---------- options, markers, run records, cleanup ----------

AGENT_RUNS = []        # one record per Claude Code call: case, command, seconds, cost, tokens
PROJECTS = {}          # test-node key -> temporary project folder
FAILED_KEYS = set()


def pytest_addoption(parser):
    parser.addoption("--run-agent", action="store_true", default=False,
                     help="also run the tests that call Claude Code (slow, costs money)")
    parser.addoption("--keep-projects", action="store_true", default=False,
                     help="keep the temporary Spec Kit projects even when the tests pass")


def pytest_configure(config):
    config.addinivalue_line("markers", "agent: calls Claude Code; runs only with --run-agent")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-agent"):
        return
    skip = pytest.mark.skip(reason="calls Claude Code; add --run-agent to run it")
    for item in items:
        if "agent" in item.keywords:
            item.add_marker(skip)


def project_key(item_or_request):
    """Tests that share one project share a key: module + case."""
    node = item_or_request.node if hasattr(item_or_request, "node") else item_or_request
    callspec = getattr(node, "callspec", None)
    return f"{node.module.__name__}:{callspec.id if callspec else node.name}"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        FAILED_KEYS.add(project_key(item))


def pytest_sessionfinish(session):
    """Delete temporary projects, except those with a failed test (kept for debugging)."""
    keep_all = session.config.getoption("--keep-projects")
    for key, project in PROJECTS.items():
        if not keep_all and key not in FAILED_KEYS:
            shutil.rmtree(project.parent, ignore_errors=True)


def pytest_terminal_summary(terminalreporter, config):
    if not AGENT_RUNS:
        return
    tr = terminalreporter
    tr.section("agent runs")
    tr.write_line(f"versions: {json.dumps(tool_versions())}")
    for run in AGENT_RUNS:
        tr.write_line(f"{run['case']:<4} {run['command']:<40} exit {run['exit']}  {run['seconds']:>5}s  "
                      f"${run['cost_usd']}  in {run['input_tokens']} / out {run['output_tokens']} tokens")
    for key in sorted(FAILED_KEYS):
        if key in PROJECTS:
            tr.write_line(f"kept for debugging: {PROJECTS[key]}")


_versions = {}


def tool_versions():
    """Spec Kit, Claude Code and extension commit (testing plan, section 9)."""
    if not _versions:
        def out(cmd, cwd=None):
            try:
                r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
                return r.stdout.strip()
            except OSError:
                return "not installed"
        spec_kit = re.search(r"\d+\.\d+\.\d+\S*", out(["specify", "version"]))
        _versions["spec_kit"] = spec_kit.group(0) if spec_kit else "unknown"
        _versions["claude_code"] = out(["claude", "--version"])
        commit = out(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT)
        dirty = out(["git", "status", "--porcelain"], cwd=ROOT)
        _versions["extension_commit"] = commit + ("+local-changes" if dirty else "")
    return _versions


# ---------- temporary Spec Kit project ----------

def require(tool):
    if not shutil.which(tool):
        pytest.skip(f"'{tool}' is not installed")


def run_cli(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")


@pytest.fixture(scope="session")
def extension_copy(tmp_path_factory):
    """A copy of this checkout without git and cache folders."""
    dest = tmp_path_factory.mktemp("ext") / "speckit-epic"
    shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"))
    return dest


def init_project(project, extension, ignore_agent_tools=False):
    """Fresh Spec Kit project, then install the local checkout with `specify extension add --dev`."""
    require("specify")
    project.mkdir(parents=True, exist_ok=True)
    script = "ps" if platform.system() == "Windows" else "sh"
    init = ["specify", "init", "--here", "--force", "--non-interactive",
            "--integration", "claude", "--script", script]
    if ignore_agent_tools:
        init.append("--ignore-agent-tools")
    log = []
    for cmd in (init, ["specify", "extension", "add", str(extension), "--dev"]):
        result = run_cli(cmd, project)
        log.append(f"$ {' '.join(cmd)}\n{result.stdout}{result.stderr}")
        assert result.returncode == 0, f"{' '.join(cmd[:3])} failed:\n{result.stdout}\n{result.stderr}"
    (project / "setup-log.txt").write_text("\n".join(log), encoding="utf-8")
    return project


def new_project(request, tmp_path_factory, extension, folder):
    """Fresh project with one fixture copied into specs/NNN-name/. Returns (project, feature folder)."""
    project = init_project(tmp_path_factory.mktemp(case_id_of(folder)) / "proj", extension)
    PROJECTS[project_key(request)] = project
    feature = project / "specs" / feature_dir_name(folder)
    feature.mkdir(parents=True)
    for md in (FIXTURES / folder).glob("*.md"):
        shutil.copy2(md, feature / md.name)
    return project, feature


def run_command(project, arguments, case=""):
    """Run /speckit-epic-framework-review <arguments> headless; record exit, output, time, cost and tokens."""
    require("claude")
    prompt = f"/speckit-epic-framework-review {arguments}"
    start = time.time()
    result = subprocess.run(
        ["claude", "-p", prompt, "--permission-mode", "acceptEdits", "--allowedTools", ALLOWED_TOOLS,
         "--output-format", "json"],
        cwd=project, capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=AGENT_TIMEOUT_SECONDS,
    )
    seconds = round(time.time() - start)
    (project / "agent-output.json").write_text(result.stdout, encoding="utf-8")
    (project / "agent-stderr.txt").write_text(result.stderr, encoding="utf-8")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = {}
    usage = data.get("usage", {})
    AGENT_RUNS.append({
        "case": case, "command": arguments, "exit": result.returncode, "seconds": seconds,
        "cost_usd": round(data.get("total_cost_usd", 0) or 0, 2),
        "input_tokens": (usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
                         + usage.get("cache_creation_input_tokens", 0)),
        "output_tokens": usage.get("output_tokens", 0),
    })
    assert result.returncode == 0, f"claude exited with {result.returncode}:\n{result.stderr[-2000:]}"
    return data.get("result", result.stdout)


def file_hashes(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob("*") if p.is_file()}


# ---------- reading epic-review.md ----------

def normalize(text):
    text = re.sub(r"[*#`>\"“”]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def parse_review(text):
    """Split epic-review.md into violations: id, dimension, location, quote, why, confidence."""
    violations = []
    for block in re.split(r"\n(?=\*\*V-\d+\*\*)", text):
        head = re.match(r"\*\*(V-\d+)\*\*:\s*([A-Z]\d)", block)
        if not head:
            continue

        def field(label):
            m = re.search(rf"^- {label}:\s*(.*)$", block, re.M)
            return m.group(1).strip() if m else ""

        violations.append({
            "id": head.group(1),
            "dimension": head.group(2),
            "location": field("Location"),
            "quote": field("Quote"),
            "why": field("Why"),
            "confidence": field("Confidence").lower(),
        })
    return violations


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def matches_finding(violation, finding):
    """Testing plan, section 4: match requirement ID + EPIC dimension + evidence, not exact prose.

    Lists in expected.json are acceptable alternatives (any one is enough).
    """
    place = normalize(violation["location"] + " " + violation["quote"])
    text = normalize(violation["location"] + " " + violation["quote"] + " " + violation["why"])
    quote = normalize(violation["quote"])
    right_dimension = violation["dimension"] in as_list(finding["dimension"])
    right_place = any(normalize(r) in place for r in as_list(finding["requirement_id"]))
    right_evidence = any(normalize(e) in text or (len(quote) > 15 and quote in normalize(e))
                         for e in as_list(finding["evidence"]))
    return right_dimension and right_place and right_evidence


def quoted_parts(quote):
    """'"a" / "b"' -> ['a', 'b']. A '(missing ...)' quote has nothing to check."""
    quote = quote.strip()
    if not quote.startswith('"') or quote.lstrip('"').lower().startswith("(missing"):
        return []  # missing content: the rest is an explanation, not a quote
    quote = quote.replace('\\"', " ")  # quotation marks inside the quoted sentence
    parts = []
    for chunk in re.findall(r'"([^"]+)"', quote):
        if chunk.strip().lower().startswith("(missing"):
            continue
        # "..." marks a cut, and a literal \n joins two quoted lines
        parts += [p for p in re.split(r"\.\.\.|…|\\n", chunk) if len(p.strip()) >= 10]
    return parts
