import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(HOOKS_DIR))

import format_python  # noqa: E402
import secret_guard  # noqa: E402

FAKE_AWS_KEY = "AKIA" + "A" * 16
FAKE_GITHUB_TOKEN = "ghp_" + "a" * 36
FAKE_ANTHROPIC_KEY = "sk-ant-" + "a" * 24


def run_hook(script: str, payload: dict[str, object]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOKS_DIR / script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize("name", [".env", ".env.local", "config/.env.production"])
def test_env_files_are_forbidden(name: str) -> None:
    assert secret_guard.is_forbidden_env_file(name)


@pytest.mark.parametrize("name", [".env.example", "environment.py", "notes.env.md"])
def test_other_files_are_allowed(name: str) -> None:
    assert not secret_guard.is_forbidden_env_file(name)


@pytest.mark.parametrize("secret", [FAKE_AWS_KEY, FAKE_GITHUB_TOKEN, FAKE_ANTHROPIC_KEY])
def test_known_secret_formats_are_detected(secret: str) -> None:
    assert secret_guard.find_violations("a.py", [f"value = '{secret}'"])


def test_private_key_header_is_detected() -> None:
    header = "-----BEGIN " + "RSA PRIVATE KEY-----"
    assert secret_guard.find_violations("a.pem", [header])


def test_hardcoded_credential_is_detected() -> None:
    assignment = 'password = "' + "Zq81xT0vLm29ab" + '"'
    assert secret_guard.find_violations("a.py", [assignment])


@pytest.mark.parametrize(
    "text",
    ['password = "change-me-please"', 'token = os.environ["TOKEN"]', "def test_login(): pass"],
)
def test_placeholders_and_clean_code_pass(text: str) -> None:
    assert secret_guard.find_violations("a.py", [text]) == []


def test_extract_texts_reads_write_edit_and_multiedit() -> None:
    tool_input = {
        "content": "one",
        "new_string": "two",
        "edits": [{"new_string": "three"}, {"old_string": "ignored"}],
    }
    assert secret_guard.extract_texts(tool_input) == ["one", "two", "three"]


def test_guard_blocks_with_exit_code_2() -> None:
    result = run_hook(
        "secret_guard.py",
        {"tool_input": {"file_path": "app.py", "content": f"KEY = '{FAKE_AWS_KEY}'"}},
    )
    assert result.returncode == 2
    assert "secret_guard" in result.stderr


def test_credential_with_a_placeholder_word_later_in_the_line_is_still_detected() -> None:
    assignment = 'password = "' + "hunter2hunter2" + '"  # test'

    assert secret_guard.find_violations("a.py", [assignment])


@pytest.mark.parametrize(
    "secret",
    [
        "xoxb-" + "1" * 12,
        "AIza" + "a" * 35,
        "eyJ" + "a" * 12 + ".eyJ" + "b" * 12 + "." + "c" * 12,
    ],
)
def test_more_token_formats_are_detected(secret: str) -> None:
    assert secret_guard.find_violations("a.py", [f"value = '{secret}'"])


def test_notebook_source_is_inspected() -> None:
    texts = secret_guard.extract_texts({"new_source": f"key = '{FAKE_AWS_KEY}'"})

    assert secret_guard.find_violations("n.ipynb", texts)


@pytest.mark.parametrize("raw", ["not json", "{}", '{"tool_input": []}', '{"tool_input": null}'])
def test_guard_fails_closed_on_unreadable_input(raw: str) -> None:
    result = subprocess.run(
        [sys.executable, str(HOOKS_DIR / "secret_guard.py")],
        input=raw,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "could not be inspected" in result.stderr


def test_formatter_tolerates_unreadable_input() -> None:
    result = subprocess.run(
        [sys.executable, str(HOOKS_DIR / "format_python.py")],
        input="not json",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0


def test_guard_allows_clean_writes() -> None:
    result = run_hook(
        "secret_guard.py", {"tool_input": {"file_path": "app.py", "content": "print('ok')"}}
    )
    assert result.returncode == 0


def test_formatter_only_touches_formatted_roots(tmp_path: Path) -> None:
    api_file = tmp_path / "API-Pytest" / "a.py"
    legacy_file = tmp_path / "legacy" / "b.py"
    for file in (api_file, legacy_file):
        file.parent.mkdir(parents=True)
        file.write_text("x = 1\n", encoding="utf-8")

    assert format_python.should_format(str(api_file), str(tmp_path))
    assert not format_python.should_format(str(legacy_file), str(tmp_path))


def test_formatter_ignores_non_python_and_missing_files(tmp_path: Path) -> None:
    notes = tmp_path / "API-Pytest" / "notes.md"
    notes.parent.mkdir()
    notes.write_text("text", encoding="utf-8")

    assert not format_python.should_format(str(notes), str(tmp_path))
    assert not format_python.should_format(str(tmp_path / "API-Pytest" / "gone.py"), str(tmp_path))
