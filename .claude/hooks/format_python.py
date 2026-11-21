import json
import subprocess
import sys
from pathlib import Path

FORMATTED_ROOTS = ("API-Pytest", "agents")
RUFF_COMMANDS = (["ruff"], [sys.executable, "-m", "ruff"])
TIMEOUT_SECONDS = 30


def should_format(path: str, project_dir: str) -> bool:
    file = Path(path)
    if file.suffix != ".py" or not file.is_file():
        return False
    try:
        relative = file.resolve().relative_to(Path(project_dir).resolve())
    except ValueError:
        return False
    return relative.parts[0] in FORMATTED_ROOTS


def run_ruff_format(path: str) -> None:
    for command in RUFF_COMMANDS:
        try:
            subprocess.run(
                [*command, "format", "--", path],
                check=False,
                capture_output=True,
                timeout=TIMEOUT_SECONDS,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
        return


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        path = str(payload.get("tool_input", {}).get("file_path", ""))
        project_dir = payload.get("cwd") or "."
    except (ValueError, AttributeError):
        sys.stderr.write("format_python: unreadable hook input, nothing formatted\n")
        return 0
    if path and should_format(path, project_dir):
        run_ruff_format(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
