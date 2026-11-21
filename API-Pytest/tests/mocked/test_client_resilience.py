from typing import Any

import pytest
import requests
import responses

from tests.mocked.conftest import SleepRecorder
from weather_client import RateLimitError, UpstreamError, WeatherClient


def test_rate_limited_request_is_retried_and_succeeds(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    sleeper: SleepRecorder,
    madrid_payload: dict[str, Any],
) -> None:
    http.add(responses.GET, weather_url, json={"message": "slow down"}, status=429)
    http.add(responses.GET, weather_url, json=madrid_payload)

    assert client.current_by_city("Madrid").name == "Madrid"
    assert sleeper.delays == [0.5]


def test_retry_after_header_overrides_the_backoff(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    sleeper: SleepRecorder,
    madrid_payload: dict[str, Any],
) -> None:
    http.add(responses.GET, weather_url, status=429, headers={"Retry-After": "3"})
    http.add(responses.GET, weather_url, json=madrid_payload)

    client.current_by_city("Madrid")

    assert sleeper.delays == [3.0]


def test_retry_after_header_is_capped(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    sleeper: SleepRecorder,
    madrid_payload: dict[str, Any],
) -> None:
    http.add(responses.GET, weather_url, status=429, headers={"Retry-After": "86400"})
    http.add(responses.GET, weather_url, json=madrid_payload)

    client.current_by_city("Madrid")

    assert sleeper.delays == [30.0]


def test_non_numeric_retry_after_falls_back_to_the_backoff(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    sleeper: SleepRecorder,
    madrid_payload: dict[str, Any],
) -> None:
    http.add(
        responses.GET,
        weather_url,
        status=429,
        headers={"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"},
    )
    http.add(responses.GET, weather_url, json=madrid_payload)

    client.current_by_city("Madrid")

    assert sleeper.delays == [0.5]


def test_backoff_grows_exponentially_across_server_errors(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    sleeper: SleepRecorder,
    madrid_payload: dict[str, Any],
) -> None:
    http.add(responses.GET, weather_url, status=500)
    http.add(responses.GET, weather_url, status=502)
    http.add(responses.GET, weather_url, json=madrid_payload)

    client.current_by_city("Madrid")

    assert sleeper.delays == [0.5, 1.0]


def test_persistent_server_error_is_raised_after_exhausting_retries(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    sleeper: SleepRecorder,
) -> None:
    for _ in range(3):
        http.add(responses.GET, weather_url, json={"message": "unavailable"}, status=503)

    with pytest.raises(UpstreamError) as raised:
        client.current_by_city("Madrid")

    assert raised.value.status_code == 503
    assert len(http.calls) == 3
    assert sleeper.delays == [0.5, 1.0]


def test_persistent_rate_limit_is_raised_after_exhausting_retries(
    client: WeatherClient, http: responses.RequestsMock, weather_url: str
) -> None:
    for _ in range(3):
        http.add(responses.GET, weather_url, json={"message": "slow down"}, status=429)

    with pytest.raises(RateLimitError):
        client.current_by_city("Madrid")

    assert len(http.calls) == 3


def test_retries_can_be_disabled(
    http: responses.RequestsMock, weather_url: str, sleeper: SleepRecorder
) -> None:
    http.add(responses.GET, weather_url, status=500)
    client = WeatherClient(
        api_key="test-key", base_url="https://weather.test/data/2.5", max_retries=0, sleep=sleeper
    )

    with pytest.raises(UpstreamError):
        client.current_by_city("Madrid")

    assert len(http.calls) == 1
    assert sleeper.delays == []


def test_timeout_is_retried_and_recovers(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
) -> None:
    http.add(responses.GET, weather_url, body=requests.exceptions.ReadTimeout("timed out"))
    http.add(responses.GET, weather_url, json=madrid_payload)

    assert client.current_by_city("Madrid").name == "Madrid"
    assert len(http.calls) == 2


def test_persistent_network_failure_never_leaks_the_api_key(
    client: WeatherClient, http: responses.RequestsMock, weather_url: str
) -> None:
    leaking_error = requests.exceptions.ConnectionError(f"failed: {weather_url}?appid=test-key")
    for _ in range(3):
        http.add(responses.GET, weather_url, body=leaking_error)

    with pytest.raises(UpstreamError) as raised:
        client.current_by_city("Madrid")

    assert "test-key" not in str(raised.value)
    assert raised.value.__cause__ is None
    assert len(http.calls) == 3
