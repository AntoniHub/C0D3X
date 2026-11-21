from typing import Any

from qa_triage.models import Category, Confidence, Triage

FAKE_KEY_VALUE = "FAKEKEY" + "1234567890abcdef"

JUNIT_WITH_FAILURES = (
    '<testsuites><testsuite name="pytest" tests="4">'
    '<testcase classname="tests.live.test_x" name="test_a" time="0.1"/>'
    '<testcase classname="tests.live.test_x" name="test_b">'
    '<failure message="ConnectionError: https://h/weather?q=Madrid&amp;appid='
    + FAKE_KEY_VALUE
    + '">'
    "Traceback line 1\nrequests failed appid=" + FAKE_KEY_VALUE + "</failure></testcase>"
    '<testcase classname="tests.mocked.test_y" name="test_c">'
    '<error message="boom">trace</error></testcase>'
    '<testcase classname="tests.mocked.test_y" name="test_d">'
    '<skipped message="skip"/></testcase>'
    "</testsuite></testsuites>"
)

JUNIT_ALL_PASSING = (
    '<testsuites><testsuite name="pytest" tests="1">'
    '<testcase classname="tests.a" name="test_ok"/></testsuite></testsuites>'
)


def sample_triage() -> Triage:
    return Triage(
        category=Category.ENVIRONMENT,
        confidence=Confidence.MEDIUM,
        summary="The runner could not reach the host.",
        suspected_cause="Network egress failure.",
        next_step="Re-run and check the runner network.",
    )


class FakeResponse:
    def __init__(self, stop_reason: str | None, parsed_output: Triage | None) -> None:
        self.stop_reason = stop_reason
        self.parsed_output = parsed_output


class FakeMessages:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.calls: list[dict[str, Any]] = []

    def parse(self, *args: Any, **kwargs: Any) -> FakeResponse:  # noqa: ARG002
        self.calls.append(kwargs)
        return self.response


class FakeClient:
    def __init__(self, response: FakeResponse | None = None) -> None:
        self.messages = FakeMessages(response or FakeResponse("end_turn", sample_triage()))
