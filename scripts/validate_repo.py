#!/usr/bin/env python3
"""Validate the Lord/Serf skill pair and protocol v0.4 assets."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - dependency bootstrap path
    raise SystemExit(
        "Missing validation dependencies. Run: "
        "python -m pip install -r requirements-dev.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (ROOT / "lord", ROOT / "serf")
FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
LOCAL_REFERENCE = re.compile(r"`((?:assets|references)/[A-Za-z0-9_.\-/]+)`")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEXT_SUFFIXES = {".md", ".py", ".txt", ".yaml", ".yml"}
FORBIDDEN_ROLE_ALIASES = re.compile(
    r"\b(?:sub-?agent|child agent|master[- ]agent|execution[- ]worker|"
    r"execution agent|external agent)\b",
    re.IGNORECASE,
)
FORBIDDEN_ARTIFACT_SUFFIXES = {".bak", ".log", ".tmp", ".zip"}
FORBIDDEN_DIRECTORY_NAMES = {".git.bak", "__pycache__", ".pytest_cache"}


def fail(message: str) -> None:
    raise AssertionError(message)


def repo_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"File is not UTF-8: {repo_path(path)} ({exc})")


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(read_text(path))
    except yaml.YAMLError as exc:
        fail(f"Invalid YAML in {repo_path(path)}: {exc}")


def markdown_front_matter(path: Path) -> dict[str, Any]:
    match = FRONT_MATTER.match(read_text(path))
    if not match:
        fail(f"Missing YAML front matter: {repo_path(path)}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        fail(f"Front matter must be a mapping: {repo_path(path)}")
    return data


def repository_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and ".agents" not in path.parts
    ]


def validate_repository_hygiene() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or ".agents" in path.parts:
            continue
        if path.is_dir() and path.name in FORBIDDEN_DIRECTORY_NAMES:
            fail(f"Generated or stale directory found: {repo_path(path)}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_ARTIFACT_SUFFIXES:
            fail(f"Generated or archive artifact found: {repo_path(path)}")

    for path in repository_files():
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {
            ".editorconfig",
            ".gitattributes",
            ".gitignore",
        }:
            continue
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            fail(f"UTF-8 BOM is not allowed: {repo_path(path)}")
        text = read_text(path)
        if text and not text.endswith("\n"):
            fail(f"Missing final newline: {repo_path(path)}")

    attributes = read_text(ROOT / ".gitattributes")
    for pattern in ("*.md", "*.py", "*.yaml", "*.yml"):
        if f"{pattern} text eol=lf" not in attributes:
            fail(f".gitattributes does not enforce LF for {pattern}")


def validate_vocabulary() -> None:
    for path in repository_files():
        if path.suffix.lower() not in {".md", ".yaml", ".yml"}:
            continue
        match = FORBIDDEN_ROLE_ALIASES.search(read_text(path))
        if match:
            fail(f"Non-canonical role term '{match.group(0)}' in {repo_path(path)}")


def validate_skill(skill_dir: Path) -> None:
    skill_path = skill_dir / "SKILL.md"
    text = read_text(skill_path)
    metadata = markdown_front_matter(skill_path)
    if set(metadata) != {"name", "description"}:
        fail(f"{repo_path(skill_path)} front matter must contain only name and description")
    if metadata["name"] != skill_dir.name or not SKILL_NAME.fullmatch(metadata["name"]):
        fail(f"Invalid skill name in {repo_path(skill_path)}")
    if not isinstance(metadata["description"], str) or not metadata["description"].strip():
        fail(f"Missing skill description in {repo_path(skill_path)}")
    if len(text.splitlines()) > 500:
        fail(f"{repo_path(skill_path)} exceeds the 500-line disclosure limit")

    agent = load_yaml(skill_dir / "agents" / "openai.yaml")
    interface = agent.get("interface", {}) if isinstance(agent, dict) else {}
    required = {"display_name", "short_description", "default_prompt"}
    if not required.issubset(interface):
        fail(f"Missing UI metadata in {skill_dir.name}/agents/openai.yaml")
    description = interface["short_description"]
    if not isinstance(description, str) or not 25 <= len(description) <= 64:
        fail(f"short_description must contain 25-64 characters for {skill_dir.name}")
    if f"${skill_dir.name}" not in interface["default_prompt"]:
        fail(f"default_prompt must mention ${skill_dir.name}")

    for reference in LOCAL_REFERENCE.findall(text):
        local = skill_dir / reference
        paired = next(
            (
                other / reference
                for other in SKILLS
                if other != skill_dir and (other / reference).exists()
            ),
            None,
        )
        if not local.exists() and paired is None:
            fail(f"Broken reference in {repo_path(skill_path)}: {reference}")


def validate_yaml_and_schemas() -> dict[str, dict[str, Any]]:
    for skill_dir in SKILLS:
        for path in skill_dir.rglob("*.yaml"):
            load_yaml(path)
        for path in (skill_dir / "assets" / "templates").glob("*.md"):
            if read_text(path).startswith("---"):
                markdown_front_matter(path)

    schema_paths = {
        path.name: path
        for skill_dir in SKILLS
        for path in (skill_dir / "assets" / "schemas").glob("*.schema.yaml")
    }
    schemas: dict[str, dict[str, Any]] = {}
    for name, path in schema_paths.items():
        schema = load_yaml(path)
        Draft202012Validator.check_schema(schema)
        schemas[name] = schema
    return schemas


def validate_canonical_assets() -> None:
    required = {
        ROOT / "lord/assets/templates/task-package.md",
        ROOT / "serf/assets/templates/micro-review-report.yaml",
        ROOT / "serf/assets/templates/review-report.md",
        ROOT / "serf/assets/templates/change-request-report.md",
    }
    legacy = {
        ROOT / "lord/assets/templates/agent-task.md",
        ROOT / "lord/assets/templates/handoff.md",
        ROOT / "lord/assets/templates/blocker.md",
        ROOT / "lord/assets/templates/change-request.md",
        ROOT / "serf/assets/templates/micro-handoff.yaml",
        ROOT / "serf/assets/templates/review-handoff.md",
    }
    for path in required:
        if not path.is_file():
            fail(f"Missing canonical asset: {repo_path(path)}")
    for path in legacy:
        if path.exists():
            fail(f"Legacy asset still present: {repo_path(path)}")


def validate_template_profiles() -> None:
    cases = {
        ROOT / "lord/assets/templates/task-package.md": {"standard", "full"},
        ROOT / "lord/assets/templates/dispatch-instruction.md": {"micro", "standard", "full"},
        ROOT / "serf/assets/templates/review-report.md": {"standard", "full"},
        ROOT / "serf/assets/templates/blocker-report.md": {"micro", "standard", "full"},
        ROOT / "serf/assets/templates/change-request-report.md": {"micro", "standard", "full"},
    }
    for path, supported in cases.items():
        metadata = markdown_front_matter(path)
        if metadata.get("profile") is not None:
            fail(f"Multi-profile template hard-codes profile in {repo_path(path)}")
        match = re.search(r"^profile:\s*#\s*(.+)$", read_text(path), re.MULTILINE)
        if match is None or not all(profile in match.group(1) for profile in supported):
            fail(f"Profile choices are incomplete in {repo_path(path)}")


def validate_template_contracts() -> None:
    forbidden = {
        "agent_id",
        "assigned_to",
        "status",
        "target_agent_type",
        "required_files",
        "allowed_changes",
        "return_path",
        "handoff_path",
        "revision",
        "submission_status",
        "lord_invocation",
    }
    task_common = {
        "protocol_version",
        "profile",
        "project_id",
        "task_id",
        "task_version",
        "updated_at",
        "task_status",
    }
    submission_common = {
        "protocol_version",
        "profile",
        "project_id",
        "task_id",
        "executed_task_version",
        "submitted_at",
        "submission_type",
        "task_package_path",
        "report_path",
    }
    cases = {
        ROOT / "lord/assets/templates/micro-task.yaml": task_common
        | {"submission_path"},
        ROOT / "lord/assets/templates/task-package.md": task_common
        | {"target_adapter", "submission_path"},
        ROOT / "lord/assets/templates/dispatch-instruction.md": {
            "protocol_version",
            "profile",
            "project_id",
            "task_id",
            "task_version",
            "target_adapter",
            "task_package_path",
            "submission_path",
        },
        ROOT / "serf/assets/templates/micro-review-report.yaml": submission_common,
        ROOT / "serf/assets/templates/review-report.md": submission_common,
        ROOT / "serf/assets/templates/blocker-report.md": submission_common,
        ROOT / "serf/assets/templates/change-request-report.md": submission_common,
    }
    for path, required in cases.items():
        data = load_yaml(path) if path.suffix == ".yaml" else markdown_front_matter(path)
        keys = set(data)
        missing = required - keys
        stale = forbidden & keys
        if missing:
            fail(f"{repo_path(path)} misses canonical fields: {sorted(missing)}")
        if stale:
            fail(f"{repo_path(path)} uses legacy fields: {sorted(stale)}")


def validate_envelope_templates(envelope_schema: dict[str, Any]) -> None:
    required = set(envelope_schema["required"])
    names = ("review-report.md", "blocker-report.md", "change-request-report.md")
    for name in names:
        path = ROOT / "serf" / "assets" / "templates" / name
        missing = required - set(markdown_front_matter(path))
        if missing:
            fail(f"{repo_path(path)} misses envelope fields: {sorted(missing)}")

    commands = {
        "review-report.md": "$lord review",
        "blocker-report.md": "$lord resolve",
        "change-request-report.md": "$lord resolve",
    }
    for name, command in commands.items():
        path = ROOT / "serf" / "assets" / "templates" / name
        if command not in read_text(path):
            fail(f"Incorrect Lord command in {repo_path(path)}")


def validate_examples(schemas: dict[str, dict[str, Any]]) -> None:
    environment = {
        "requires_python": False,
        "conda_env_path": None,
        "conda_env_name": None,
        "python_executable": None,
        "activation_command": None,
        "package_install_policy": None,
    }
    task_base = {
        "protocol_version": "0.4",
        "project_id": "demo",
        "task_id": "Task-A-01",
        "task_version": "v1",
        "updated_at": "2026-06-25T15:00:00Z",
        "task_status": "READY",
    }
    common_task = {
        "objective": "Update one isolated file.",
        "inputs": [],
        "allowed_paths": ["src/example.py"],
        "forbidden_paths": [],
        "expected_outputs": ["src/example.py"],
        "acceptance_criteria": {"AC-01": "The example passes validation."},
        "validation_methods": ["python -m compileall src"],
        "depends_on": [],
        "execution_environment": environment,
    }
    micro_task = {
        **task_base,
        **common_task,
        "profile": "micro",
        "inherits": [],
        "submission_path": "REVIEWS/Task-A-01-REVIEW.yaml",
    }
    standard_task = {
        **task_base,
        **common_task,
        "profile": "standard",
        "target_adapter": "coding",
        "dispatch_mode": "direct",
        "authoritative_state_source": "PROJECT_PLAN.md",
        "submission_path": "REVIEWS/Task-A-01-REVIEW.md",
    }
    dispatch = {
        "protocol_version": "0.4",
        "profile": "standard",
        "project_id": "demo",
        "task_id": "Task-A-01",
        "task_version": "v1",
        "target_adapter": "coding",
        "dispatch_mode": "direct",
        "generated_at": "2026-06-25T15:05:00Z",
        "task_package_path": "TASKS/Task-A-01.md",
        "submission_path": "REVIEWS/Task-A-01-REVIEW.md",
        "worker_skill": "serf",
        "worker_invocation": "$serf",
    }
    envelope = {
        "protocol_version": "0.4",
        "profile": "standard",
        "project_id": "demo",
        "task_id": "Task-A-01",
        "executed_task_version": "v1",
        "submitted_at": "2026-06-25T15:30:00Z",
        "submission_type": "REVIEW",
        "task_package_path": "TASKS/Task-A-01.md",
        "report_path": "REVIEWS/Task-A-01-REVIEW.md",
    }
    report_fields = {
        "changed_outputs": ["src/example.py"],
        "results": ["Implemented the requested change."],
        "validation_results": {
            "AC-01": {"result": "PASS", "evidence": "1 test passed"}
        },
        "assumptions": [],
        "issues": [],
    }
    micro_report = {
        **envelope,
        **report_fields,
        "profile": "micro",
        "task_package_path": "TASKS/Task-A-01.yaml",
        "report_path": "REVIEWS/Task-A-01-REVIEW.yaml",
    }
    full_report = {**envelope, **report_fields, "profile": "full"}
    examples = {
        "micro-task.schema.yaml": micro_task,
        "task-package.schema.yaml": standard_task,
        "dispatch-instruction.schema.yaml": dispatch,
        "submission-envelope.schema.yaml": envelope,
        "micro-review-report.schema.yaml": micro_report,
        "review-report.schema.yaml": full_report,
    }
    checker = FormatChecker()
    for schema_name, instance in examples.items():
        Draft202012Validator(schemas[schema_name], format_checker=checker).validate(instance)


def main() -> int:
    validate_repository_hygiene()
    validate_vocabulary()
    for skill_dir in SKILLS:
        validate_skill(skill_dir)
    schemas = validate_yaml_and_schemas()
    validate_canonical_assets()
    validate_template_profiles()
    validate_template_contracts()
    validate_envelope_templates(schemas["submission-envelope.schema.yaml"])
    validate_examples(schemas)
    print("Validated Lord/Serf protocol v0.4, repository hygiene, and canonical vocabulary.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
