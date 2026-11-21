from pathlib import Path

import pytest
from defusedxml import EntitiesForbidden

from qa_triage.junit import MAX_DETAILS_CHARS, parse_failures
from tests.fakes import FAKE_KEY_VALUE


def test_failures_and_errors_are_returned_and_the_rest_ignored(junit_file: Path) -> None:
    failures = parse_failures(junit_file)

    assert [f.test_id for f in failures] == [
        "tests.live.test_x::test_b",
        "tests.mocked.test_y::test_c",
    ]


def test_secrets_never_leave_the_parser(junit_file: Path) -> None:
    failure = parse_failures(junit_file)[0]

    assert FAKE_KEY_VALUE not in failure.message
    assert FAKE_KEY_VALUE not in failure.details


def test_a_run_without_failures_gives_an_empty_list(passing_junit_file: Path) -> None:
    assert parse_failures(passing_junit_file) == []


def test_details_are_truncated(tmp_path: Path) -> None:
    path = tmp_path / "long.xml"
    body = "x" * (MAX_DETAILS_CHARS * 2)
    path.write_text(
        f'<testsuite><testcase classname="a" name="b"><failure message="m">{body}</failure>'
        "</testcase></testsuite>",
        encoding="utf-8",
    )

    assert len(parse_failures(path)[0].details) == MAX_DETAILS_CHARS


def test_xml_entities_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "hostile.xml"
    path.write_text(
        '<?xml version="1.0"?><!DOCTYPE t [<!ENTITY e "expanded">]>'
        '<testsuite><testcase classname="a" name="b">'
        '<failure message="&e;"/></testcase></testsuite>',
        encoding="utf-8",
    )

    with pytest.raises(EntitiesForbidden):
        parse_failures(path)
