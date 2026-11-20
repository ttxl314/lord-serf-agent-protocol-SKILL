#!/usr/bin/env python3
"""Validate the Lord/Serf skill pair and protocol v0.6 assets."""

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
PROTOCOL_VERSION = "0.6"
FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
LOCAL_REFERENCE = re.compile(r"`((?:assets|references)/[A-Za-z0-9_.\-/]+)`")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEXT_SUFFIXES = {".md", ".py", ".txt", ".yaml", ".yml"}
# "subagent" is a host tool name, not a protocol role, so only the hyphenated
# and competing-role spellings are rejected here.
FORBIDDEN_ROLE_ALIASES = re.compile(
    r"\b(?:sub-agent|child agent|master[- ]agent|execution[- ]worker|"
    r"execution agent|external agent)\b",
    re.IGNORECASE,
)
FORBIDDEN_ARTIFACT_SUFFIXES = {".bak", ".log", ".tmp", ".zip"}
FORBIDDEN_DIRECTORY_NAMES = {".git.bak", "__pycache__", ".pytest_cache"}
LEGACY_FIELDS = {
    "acceptance",
    "agent_id",
    "allowed_changes",
    "assigned_to",
    "change_status",
    "changed",
    "handoff_path",
    "lord_invocation",
    "required_files",
    "result",
    "return_path",
    "revision",
    "status",
    "submission_status",
    "target_agent_type",
    "validation",
}
TEMPLATE_SCHEMAS = {
    "lord/assets/templates/micro-task.yaml": "micro-task.schema.yaml",
    "lord/assets/templates/task-package.md": "task-package.schema.yaml",
    "lord/assets/templates/dispatch-instruction.md": "dispatch-instruction.schema.yaml",
    "serf/assets/templates/micro-review-report.yaml": "micro-review-report.schema.yaml",
    "serf/assets/templates/review-report.md": "submission-envelope.schema.yaml",
    "serf/assets/templates/blocker-report.md": "submission-envelope.schema.yaml",
    "serf/assets/templates/change-request-report.md": "submission-envelope.schema.yaml",
}
TASK_PACKAGE_BODY_FIELDS = {
    "acceptance_criteria",
    "allowed_paths",
    "forbidden_paths",
    "inputs",
    "objective",
    "expected_outputs",
    "validation_methods",
}
COORDINATION_REFERENCES = {
    "lord": (
        "references/host-runtimes.md",
        "references/cross-application-handoff.md",
        "references/intra-app-parallelism.md",
    ),
    "serf": (
        "references/host-runtimes.md",
        "references/cross-application-handoff.md",
        "references/parallel-worker.md",
    ),
}
HOST_BLOCKS = ("host:", "handoff:")
HOST_PLATFORMS = ("Claude Code", "Codex", "DSH")


def fail(message: str) -> None:
    raise AssertionError(message)


def repo_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"Required file not found: {repo_path(path)}")
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
        if b"\r\n" in raw:
            fail(f"CRLF line endings are not allowed: {repo_path(path)}")
        text = read_text(path)
        if text and not text.endswith("\n"):
            fail(f"Missing final newline: {repo_path(path)}")

    attributes = read_text(ROOT / ".gitattributes")
    for pattern in ("*.md", "*.py", "*.txt", "*.yaml", "*.yml"):
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
    if len(" ".join(metadata["description"].split())) > 1024:
        fail(f"{repo_path(skill_path)} description exceeds 1024 characters")
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


def validate_reference_index() -> None:
    for skill_dir in SKILLS:
        index = read_text(skill_dir / "SKILL.md")
        if "## Hosts" not in index:
            fail(f"{skill_dir.name}/SKILL.md must contain a Hosts section")
        for folder in ("references", "assets"):
            base = skill_dir / folder
            if not base.is_dir():
                fail(f"Missing directory: {repo_path(base)}")
            for path in sorted(base.rglob("*")):
                if path.is_file() and path.name not in index:
                    fail(f"{repo_path(path)} is not indexed by {skill_dir.name}/SKILL.md")


def validate_template_headings() -> None:
    for skill_dir in SKILLS:
        for path in sorted((skill_dir / "assets" / "templates").glob("*.md")):
            text = read_text(path)
            front = FRONT_MATTER.match(text)
            body = text[front.end() :] if front else text
            headings = re.findall(r"(?m)^# (.+)$", body)
            if len(headings) != 1:
                fail(
                    f"{repo_path(path)} must contain exactly one level-one heading, "
                    f"found {len(headings)}"
                )
            if any("command" in heading.lower() for heading in headings):
                fail(f"{repo_path(path)} embeds a chat command heading")
            if skill_dir.name != "serf":
                continue
            for token in ("$lord", "$serf"):
                if token in body:
                    fail(
                        f"{repo_path(path)} stores the chat command '{token}' "
                        "in the report body"
                    )


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
        ROOT / "lord/assets/templates/dispatch-instruction.md",
        ROOT / "lord/assets/templates/micro-task.yaml",
        ROOT / "lord/assets/templates/task-package.md",
        ROOT / "serf/assets/templates/blocker-report.md",
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


def validate_coordination_assets(schemas: dict[str, dict[str, Any]]) -> None:
    for skill_dir in SKILLS:
        for relative in COORDINATION_REFERENCES[skill_dir.name]:
            if not (skill_dir / relative).is_file():
                fail(f"Missing coordination reference: {skill_dir.name}/{relative}")

    dispatch_properties = schemas["dispatch-instruction.schema.yaml"].get("properties", {})
    for block in ("host", "handoff"):
        if block not in dispatch_properties:
            fail(f"dispatch-instruction.schema.yaml misses the optional '{block}' block")
        if not isinstance(dispatch_properties[block], dict):
            fail(f"dispatch-instruction.schema.yaml '{block}' must be an object schema")

    template = read_text(ROOT / "lord/assets/templates/dispatch-instruction.md")
    for marker in HOST_BLOCKS:
        if marker not in template:
            fail(f"dispatch-instruction.md does not document the '{marker}' block")

    enveloped = {
        "submission-envelope.schema.yaml": schemas["submission-envelope.schema.yaml"],
        "micro-review-report.schema.yaml": schemas["micro-review-report.schema.yaml"],
        "review-report.schema.yaml": schemas["review-report.schema.yaml"],
    }
    for name, schema in enveloped.items():
        if "execution_host" not in schema.get("properties", {}):
            fail(f"{name} misses the optional execution_host field")

    for skill_dir in SKILLS:
        hosts = read_text(skill_dir / "references" / "host-runtimes.md")
        for platform in HOST_PLATFORMS:
            if platform not in hosts:
                fail(f"{skill_dir.name}/references/host-runtimes.md misses {platform}")


def validate_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    if not path.is_file():
        fail("Missing CHANGELOG.md")
    text = read_text(path)
    if not text.startswith("# Changelog"):
        fail("CHANGELOG.md must start with '# Changelog'")
    release = re.search(r"(?m)^## (\d+\.\d+(?:\.\d+)?)\s*$", text)
    if not release:
        fail("CHANGELOG.md must contain a '## <version>' release heading")
    if not release.group(1).startswith(f"{PROTOCOL_VERSION}."):
        fail(
            "CHANGELOG.md latest release heading must belong to protocol "
            f"{PROTOCOL_VERSION}, found {release.group(1)}"
        )


def validate_project_context_index() -> None:
    required_markers = {
        ROOT / "lord/assets/templates/task-package.md": (
            "### Project Context Index",
            "- Project goal:",
            "- This task's role:",
            "- Related task IDs:",
            "- Alignment files (repo-root paths only):",
        ),
        ROOT / "lord/assets/templates/micro-task.yaml": (
            "connect the project goal to this task's contribution",
            "# Upstream task IDs that affect this task.",
            "interfaces needed for alignment",
        ),
    }
    for path, markers in required_markers.items():
        text = read_text(path)
        missing = [marker for marker in markers if marker not in text]
        if missing:
            fail(f"{repo_path(path)} misses project context index markers: {missing}")


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
        front = FRONT_MATTER.match(read_text(path))
        haystack = front.group(0) if front else read_text(path)
        match = re.search(r"^profile:\s*#\s*(.+?)\s*$", haystack, re.MULTILINE)
        declared = (
            {part.strip() for part in match.group(1).split("|") if part.strip()}
            if match
            else set()
        )
        if declared != supported:
            fail(f"Profile choices are incomplete in {repo_path(path)}")


def validate_template_contracts(schemas: dict[str, dict[str, Any]]) -> None:
    checker = FormatChecker()
    for relative_path, schema_name in TEMPLATE_SCHEMAS.items():
        path = ROOT / relative_path
        data = load_yaml(path) if path.suffix == ".yaml" else markdown_front_matter(path)
        schema = schemas[schema_name]
        required = set(schema["required"])
        if relative_path == "lord/assets/templates/task-package.md":
            required -= TASK_PACKAGE_BODY_FIELDS
        keys = set(data)
        missing = required - keys
        stale = LEGACY_FIELDS & keys
        if missing:
            fail(f"{repo_path(path)} misses canonical fields: {sorted(missing)}")
        if stale:
            fail(f"{repo_path(path)} uses legacy fields: {sorted(stale)}")

        for key, value in data.items():
            property_schema = schema.get("properties", {}).get(key)
            if property_schema is None:
                continue
            if value is None:
                if key not in required:
                    fail(
                        f"{repo_path(path)} carries optional field '{key}' with an "
                        "empty value; comment it out instead"
                    )
                continue
            if value == [] or value == {}:
                continue
            field_schema = {
                "$schema": schema.get("$schema"),
                "$defs": schema.get("$defs", {}),
                "type": "object",
                "required": [key],
                "properties": {key: property_schema},
                "additionalProperties": False,
            }
            error = next(
                Draft202012Validator(
                    field_schema, format_checker=checker
                ).iter_errors({key: value}),
                None,
            )
            if error:
                fail(
                    f"{repo_path(path)} field '{key}' violates {schema_name}: "
                    f"{error.message}"
                )


def validate_envelope_templates(envelope_schema: dict[str, Any]) -> None:
    required = set(envelope_schema["required"])
    names = ("review-report.md", "blocker-report.md", "change-request-report.md")
    for name in names:
        path = ROOT / "serf" / "assets" / "templates" / name
        missing = required - set(markdown_front_matter(path))
        if missing:
            fail(f"{repo_path(path)} misses envelope fields: {sorted(missing)}")

    # Routing belongs to chat and is documented once, in the reporting reference.
    reporting = read_text(ROOT / "serf" / "references" / "submission-reporting.md")
    for command in ("$lord review", "$lord resolve"):
        if command not in reporting:
            fail(f"submission-reporting.md does not document '{command}'")


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
        "protocol_version": PROTOCOL_VERSION,
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
        "protocol_version": PROTOCOL_VERSION,
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
        "worker_invocation": 'skill("serf")',
        "host": {
            "agent": "dsh",
            "model": "deepseek-flash",
            "skill_invocation": 'skill("serf")',
            "supports_subagents": True,
            "shared_workspace": True,
        },
        "handoff": {
            "from_app": "dsh",
            "to_app": "word",
            "transport": "upload",
            "return_transport": "upload",
        },
    }
    envelope = {
        "protocol_version": PROTOCOL_VERSION,
        "profile": "standard",
        "project_id": "demo",
        "task_id": "Task-A-01",
        "executed_task_version": "v1",
        "submitted_at": "2026-06-25T15:30:00Z",
        "submission_type": "REVIEW",
        "task_package_path": "TASKS/Task-A-01.md",
        "report_path": "REVIEWS/Task-A-01-REVIEW.md",
        "execution_host": "dsh",
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
        validator = Draft202012Validator(schemas[schema_name], format_checker=checker)
        validator.validate(instance)
        if not list(validator.iter_errors({**instance, "protocol_version": "0.5"})):
            fail(f"{schema_name} accepts obsolete protocol version 0.5")

    dispatch_validator = Draft202012Validator(
        schemas["dispatch-instruction.schema.yaml"], format_checker=checker
    )
    bad_transport = {
        **dispatch,
        "handoff": {**dispatch["handoff"], "transport": "email"},
    }
    if not list(dispatch_validator.iter_errors(bad_transport)):
        fail("dispatch-instruction.schema.yaml accepts an unknown handoff transport")
    bad_agent = {**dispatch, "host": {**dispatch["host"], "agent": "unknown-app"}}
    if not list(dispatch_validator.iter_errors(bad_agent)):
        fail("dispatch-instruction.schema.yaml accepts an unknown host agent")

    envelope_validator = Draft202012Validator(
        schemas["submission-envelope.schema.yaml"], format_checker=checker
    )
    envelope_variants = (
        envelope,
        {
            **envelope,
            "submission_type": "BLOCKED",
            "report_path": "BLOCKERS/Task-A-01-BLOCKER.md",
        },
        {
            **envelope,
            "profile": "full",
            "submission_type": "CHANGE_REQUEST",
            "report_path": "CHANGE_REQUESTS/Task-A-01-CHANGE-REQUEST.md",
        },
    )
    for instance in envelope_variants:
        envelope_validator.validate(instance)
        for field in LEGACY_FIELDS:
            if not list(envelope_validator.iter_errors({**instance, field: "legacy"})):
                fail(
                    "submission-envelope.schema.yaml accepts legacy field "
                    f"'{field}' for {instance['submission_type']}"
                )


def main() -> int:
    validate_repository_hygiene()
    validate_vocabulary()
    for skill_dir in SKILLS:
        validate_skill(skill_dir)
    validate_reference_index()
    validate_template_headings()
    schemas = validate_yaml_and_schemas()
    validate_canonical_assets()
    validate_coordination_assets(schemas)
    validate_changelog()
    validate_project_context_index()
    validate_template_profiles()
    validate_template_contracts(schemas)
    validate_envelope_templates(schemas["submission-envelope.schema.yaml"])
    validate_examples(schemas)
    print(
        f"Validated Lord/Serf protocol v{PROTOCOL_VERSION}, repository hygiene, "
        "canonical vocabulary, host and handoff assets."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
