from pathlib import Path

import anthropic
import pytest

from qa_triage import cli
from tests.fakes import FakeClient, FakeResponse


def forbid_model_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail() -> None:
        raise AssertionError("the model client must not be created")

    monkeypatch.setattr(anthropic, "Anthropic", fail)


def test_fingerprint_command_prints_the_hash(
    junit_file: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["fingerprint", str(junit_file)]) == 0

    assert len(capsys.readouterr().out.strip()) == 12


def test_several_reports_are_combined(
    junit_file: Path,
    passing_junit_file: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(cli.API_KEY_VARIABLE, raising=False)

    cli.main(["triage", str(passing_junit_file), str(junit_file)])

    assert "2 failing test(s)" in capsys.readouterr().out


def test_fingerprint_command_reports_none_for_a_green_run(
    passing_junit_file: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    cli.main(["fingerprint", str(passing_junit_file)])

    assert capsys.readouterr().out.strip() == "none"


def test_green_run_needs_no_triage(
    passing_junit_file: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    forbid_model_calls(monkeypatch)

    assert cli.main(["triage", str(passing_junit_file)]) == 0

    assert "No failures found" in capsys.readouterr().err


def test_dry_run_never_calls_the_model(
    junit_file: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    forbid_model_calls(monkeypatch)
    monkeypatch.setenv(cli.API_KEY_VARIABLE, "present")
    out = tmp_path / "issue.md"

    assert cli.main(["triage", str(junit_file), "--dry-run", "--out", str(out)]) == 0

    assert "not triaged" in out.read_text(encoding="utf-8")


def test_missing_key_skips_the_model_and_still_succeeds(
    junit_file: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    forbid_model_calls(monkeypatch)
    monkeypatch.delenv(cli.API_KEY_VARIABLE, raising=False)

    assert cli.main(["triage", str(junit_file)]) == 0

    captured = capsys.readouterr()
    assert f"{cli.API_KEY_VARIABLE} is not set" in captured.err
    assert "# Test failures triage" in captured.out


def test_triage_uses_the_model_named_in_the_environment(
    junit_file: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    client = FakeClient()
    monkeypatch.setenv(cli.API_KEY_VARIABLE, "present")
    monkeypatch.setenv(cli.MODEL_VARIABLE, "custom-model")
    monkeypatch.setattr(anthropic, "Anthropic", lambda: client)

    assert cli.main(["triage", str(junit_file)]) == 0

    assert {call["model"] for call in client.messages.calls} == {"custom-model"}
    assert "| environment | medium |" in capsys.readouterr().out


def test_a_failed_classification_is_reported_and_does_not_abort(
    junit_file: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    client = FakeClient(FakeResponse("refusal", None))
    monkeypatch.setenv(cli.API_KEY_VARIABLE, "present")
    monkeypatch.setattr(anthropic, "Anthropic", lambda: client)

    assert cli.main(["triage", str(junit_file)]) == 0

    captured = capsys.readouterr()
    assert "Could not triage" in captured.err
    assert "not triaged" in captured.out


@pytest.mark.parametrize("value", ["0", "-1", "many"])
def test_max_failures_must_be_a_positive_integer(junit_file: Path, value: str) -> None:
    with pytest.raises(SystemExit) as exit_info:
        cli.main(["triage", str(junit_file), "--max-failures", value])

    assert exit_info.value.code == 2


def test_a_missing_report_is_an_input_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["triage", str(tmp_path / "missing.xml")]) == cli.INPUT_ERROR_EXIT_CODE

    assert "Could not process the reports" in capsys.readouterr().err


def test_a_malformed_report_is_an_input_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    broken = tmp_path / "broken.xml"
    broken.write_text("<testsuite><testcase", encoding="utf-8")

    assert cli.main(["fingerprint", str(broken)]) == cli.INPUT_ERROR_EXIT_CODE

    assert "ParseError" in capsys.readouterr().err


def test_max_failures_limits_the_triaged_set(
    junit_file: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(cli.API_KEY_VARIABLE, raising=False)

    cli.main(["triage", str(junit_file), "--max-failures", "1"])

    assert capsys.readouterr().out.count("\n## ") == 1
