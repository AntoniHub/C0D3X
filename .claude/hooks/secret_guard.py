import json
import re
import sys
from pathlib import Path
from typing import Any

SECRET_PATTERNS: dict[str, re.Pattern[str]] = {
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "Anthropic API key": re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    "API key": re.compile(r"sk-[A-Za-z0-9]{32,}"),
    "Slack token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "Google API key": re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    "JSON web token": re.compile(
        r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
    ),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}
CREDENTIAL_ASSIGNMENT = re.compile(
    r"""(?i)\b(?:password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*["']([^"'\s]{12,})["']"""
)
PLACEHOLDER_VALUE = re.compile(r"(?i)change|example|placeholder|dummy|fake|test|<|\$\{")
ENV_FILE_NAME = re.compile(r"^\.env(\..+)?$")
ALLOWED_ENV_FILES = {".env.example"}
TEXT_FIELDS = ("content", "new_string", "new_source")
BLOCK_EXIT_CODE = 2


def is_forbidden_env_file(path: str) -> bool:
    name = Path(path).name
    return bool(ENV_FILE_NAME.match(name)) and name not in ALLOWED_ENV_FILES


def extract_texts(tool_input: dict[str, Any]) -> list[str]:
    texts = [str(tool_input[field]) for field in TEXT_FIELDS if field in tool_input]
    for edit in tool_input.get("edits", []):
        texts.extend(str(edit[field]) for field in TEXT_FIELDS if field in edit)
    return texts


def has_hardcoded_credential(text: str) -> bool:
    return any(
        not PLACEHOLDER_VALUE.search(match.group(1))
        for match in CREDENTIAL_ASSIGNMENT.finditer(text)
    )


def find_violations(path: str, texts: list[str]) -> list[str]:
    violations: list[str] = []
    if path and is_forbidden_env_file(path):
        violations.append(f"writing {Path(path).name} is not allowed")
    for label, pattern in SECRET_PATTERNS.items():
        if any(pattern.search(text) for text in texts):
            violations.append(f"content looks like a {label}")
    if any(has_hardcoded_credential(text) for text in texts):
        violations.append("content looks like a hardcoded credential")
    return violations


def block(reason: str) -> int:
    sys.stderr.write(f"Blocked by secret_guard: {reason}\n")
    return BLOCK_EXIT_CODE


def main() -> int:
    try:
        tool_input = json.load(sys.stdin)["tool_input"]
        violations = find_violations(
            str(tool_input.get("file_path", "")), extract_texts(tool_input)
        )
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        return block(f"the call could not be inspected ({type(exc).__name__})")
    return block("; ".join(violations)) if violations else 0


if __name__ == "__main__":
    sys.exit(main())
