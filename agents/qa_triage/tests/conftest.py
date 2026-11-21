from pathlib import Path

import pytest

from tests.fakes import JUNIT_ALL_PASSING, JUNIT_WITH_FAILURES


@pytest.fixture
def junit_file(tmp_path: Path) -> Path:
    path = tmp_path / "report.xml"
    path.write_text(JUNIT_WITH_FAILURES, encoding="utf-8")
    return path


@pytest.fixture
def passing_junit_file(tmp_path: Path) -> Path:
    path = tmp_path / "passing.xml"
    path.write_text(JUNIT_ALL_PASSING, encoding="utf-8")
    return path
