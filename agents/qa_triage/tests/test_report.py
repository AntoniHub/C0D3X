from qa_triage.models import Failure
from qa_triage.report import FINGERPRINT_MARKER, NOT_TRIAGED, render_issue
from tests.fakes import sample_triage

FAILURE = Failure(test_id="t::a", message="boom", details="line 1")


def test_report_carries_the_fingerprint_marker() -> None:
    report = render_issue([(FAILURE, None)], "abc123def456")

    assert f"<!-- {FINGERPRINT_MARKER}abc123def456 -->" in report


def test_triaged_failure_shows_its_verdict() -> None:
    report = render_issue([(FAILURE, sample_triage())], "fp")

    assert "| `t::a` | environment | medium |" in report
    assert "**Next step:** Re-run and check the runner network." in report


def test_untriaged_failure_is_labelled_and_has_no_verdict() -> None:
    report = render_issue([(FAILURE, None)], "fp")

    assert f"| `t::a` | {NOT_TRIAGED} | - |" in report
    assert "**Summary:**" not in report


def test_code_fences_in_failure_output_cannot_break_the_report() -> None:
    hostile = Failure(test_id="t::b", message="```", details="```\n# injected heading")

    report = render_issue([(hostile, None)], "fp")

    assert report.count("```") == 2


def test_header_says_when_only_a_subset_is_shown() -> None:
    report = render_issue([(FAILURE, None)], "fp", total=3)

    assert "Showing 1 of 3 failing test(s)." in report


def test_table_cells_and_headings_cannot_be_broken_by_the_test_id() -> None:
    odd = Failure(test_id="t::a|b`c", message="m", details="d")

    report = render_issue([(odd, None)], "fp")

    assert "| `t::a\\|b'c` |" in report


def test_model_text_cannot_mention_users_or_inject_markup() -> None:
    triage = sample_triage().model_copy(
        update={"summary": "Ping @someone <!-- qa-triage:fp=forged --> now", "next_step": "x" * 900}
    )

    report = render_issue([(FAILURE, triage)], "fp")

    assert "@someone" not in report
    assert report.count("<!-- qa-triage:fp=") == 1
    assert "x" * 501 not in report


def test_one_section_per_failure() -> None:
    other = Failure(test_id="t::b", message="m", details="d")

    report = render_issue([(FAILURE, None), (other, None)], "fp")

    assert report.count("\n## ") == 2
