from typing import Any

import pytest
from pydantic import ValidationError

from weather_client import Settings
from weather_client.config import DEFAULT_BASE_URL, MAX_TIMEOUT_SECONDS

ENVIRONMENT_VARIABLES = ("OWM_API_KEY", "OWM_BASE_URL", "OWM_TIMEOUT_SECONDS")


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(name, raising=False)


def build(**values: Any) -> Settings:
    return Settings(_env_file=None, **values)


def rejected_fields(**values: Any) -> list[str]:
    with pytest.raises(ValidationError) as exc_info:
        build(**values)
    return [str(error["loc"][0]) for error in exc_info.value.errors()]


def test_defaults_are_safe() -> None:
    settings = build()

    assert settings.owm_base_url == DEFAULT_BASE_URL
    assert settings.owm_timeout_seconds == 10.0


@pytest.mark.parametrize("timeout", [0, -1, MAX_TIMEOUT_SECONDS + 1, float("inf"), float("nan")])
def test_rejects_unreasonable_timeouts(timeout: float) -> None:
    assert rejected_fields(owm_timeout_seconds=timeout) == ["owm_timeout_seconds"]


@pytest.mark.parametrize(
    "url",
    ["http://api.example.com", "api.example.com", "ftp://example.com", "https://", "https:///v1"],
)
def test_rejects_base_urls_that_are_not_https_with_a_host(url: str) -> None:
    assert rejected_fields(owm_base_url=url) == ["owm_base_url"]


@pytest.mark.parametrize("value", ["", "   "])
def test_blank_api_key_counts_as_missing(value: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OWM_API_KEY", value)

    assert build().owm_api_key is None
    assert build(owm_api_key=value).owm_api_key is None


def test_a_real_api_key_is_kept_and_hidden_from_repr() -> None:
    settings = build(owm_api_key="abc123")

    assert settings.owm_api_key is not None
    assert settings.owm_api_key.get_secret_value() == "abc123"
    assert "abc123" not in repr(settings)


def test_base_url_is_normalised() -> None:
    assert (
        build(owm_base_url="https://api.example.com/v1/").owm_base_url
        == "https://api.example.com/v1"
    )
