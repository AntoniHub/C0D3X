from typing import Any

import pytest
import responses

from tests.mocked.conftest import SleepRecorder
from weather_client import (
    AuthenticationError,
    InvalidRequestError,
    LocationNotFoundError,
    WeatherApiError,
    WeatherClient,
)


@pytest.mark.parametrize(
    ("status", "body", "expected"),
    [
        (400, {"cod": "400", "message": "Nothing to geocode"}, InvalidRequestError),
        (401, {"cod": 401, "message": "Invalid API key."}, AuthenticationError),
        (404, {"cod": "404", "message": "city not found"}, LocationNotFoundError),
    ],
)
def test_client_errors_are_mapped_and_never_retried(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    sleeper: SleepRecorder,
    status: int,
    body: dict[str, Any],
    expected: type[WeatherApiError],
) -> None:
    http.add(responses.GET, weather_url, json=body, status=status)

    with pytest.raises(expected) as raised:
        client.current_by_city("Madrid")

    assert raised.value.status_code == status
    assert raised.value.message == body["message"]
    assert len(http.calls) == 1
    assert sleeper.delays == []


def test_non_json_error_body_falls_back_to_a_generic_message(
    client: WeatherClient, http: responses.RequestsMock, weather_url: str
) -> None:
    http.add(responses.GET, weather_url, body="<html>Not Found</html>", status=404)

    with pytest.raises(LocationNotFoundError, match="status 404"):
        client.current_by_city("Madrid")


def test_unexpected_status_maps_to_the_base_error(
    client: WeatherClient, http: responses.RequestsMock, weather_url: str
) -> None:
    http.add(responses.GET, weather_url, json={"message": "teapot"}, status=418)

    with pytest.raises(WeatherApiError) as raised:
        client.current_by_city("Madrid")

    assert type(raised.value) is WeatherApiError
    assert raised.value.status_code == 418
