from pathlib import Path
from xml.etree.ElementTree import Element  # noqa: S405

from defusedxml import ElementTree

from qa_triage.models import Failure
from qa_triage.redact import redact

MAX_DETAILS_CHARS = 4000
MAX_MESSAGE_CHARS = 1000
_PROBLEM_TAGS = ("failure", "error")


def parse_failures(path: Path) -> list[Failure]:
    root = ElementTree.parse(path).getroot()
    failures: list[Failure] = []
    if root is None:
        return failures
    for case in root.iter("testcase"):
        problem = _find_problem(case)
        if problem is not None:
            failures.append(_to_failure(case, problem))
    return failures


def _find_problem(case: Element) -> Element | None:
    for tag in _PROBLEM_TAGS:
        problem = case.find(tag)
        if problem is not None:
            return problem
    return None


def _test_id(case: Element) -> str:
    classname, name = case.get("classname", ""), case.get("name", "")
    return f"{classname}::{name}" if classname else name


def _to_failure(case: Element, problem: Element) -> Failure:
    return Failure(
        test_id=redact(_test_id(case)),
        message=redact(problem.get("message", ""))[:MAX_MESSAGE_CHARS],
        details=redact(problem.text or "")[:MAX_DETAILS_CHARS],
    )
