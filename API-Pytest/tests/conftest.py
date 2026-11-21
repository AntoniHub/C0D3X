import json
from pathlib import Path
from typing import Any

import pytest

TESTS_DIR = Path(__file__).parent
SCHEMA_PATH = TESTS_DIR.parent / "schemas" / "current_weather.schema.json"
SAMPLE_PATH = TESTS_DIR / "data" / "current_weather_madrid.json"


def pytest_html_report_title(report: Any) -> None:
    report.title = "Weather API test report"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        parts = Path(str(item.path)).relative_to(TESTS_DIR).parts
        if "live" in parts:
            item.add_marker(pytest.mark.live)
        elif "mocked" in parts:
            item.add_marker(pytest.mark.mocked)


@pytest.fixture(scope="session")
def current_weather_schema() -> dict[str, Any]:
    schema: dict[str, Any] = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return schema


@pytest.fixture
def madrid_payload() -> dict[str, Any]:
    payload: dict[str, Any] = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return payload
