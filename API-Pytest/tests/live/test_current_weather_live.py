import time
from typing import Any

import pytest
import requests
from jsonschema import Draft202012Validator

from tests.live.conftest import Fetch
from weather_client import Settings, WeatherClient

ONE_DAY_SECONDS = 24 * 60 * 60
MIN_PLAUSIBLE_CELSIUS = -90.0
MAX_PLAUSIBLE_CELSIUS = 60.0


def test_city_query_returns_a_json_success_response(madrid_metric: requests.Response) -> None:
    assert madrid_metric.status_code == 200
    assert madrid_metric.headers["Content-Type"].startswith("application/json")


def test_city_query_response_conforms_to_the_schema(
    madrid_metric: requests.Response, current_weather_schema: dict[str, Any]
) -> None:
    Draft202012Validator(current_weather_schema).validate(madrid_metric.json())


def test_city_query_resolves_to_madrid_spain(madrid_metric: requests.Response) -> None:
    body = madrid_metric.json()

    assert body["name"] == "Madrid"
    assert body["sys"]["country"] == "ES"


def test_metric_temperature_is_physically_plausible(madrid_metric: requests.Response) -> None:
    main = madrid_metric.json()["main"]

    assert MIN_PLAUSIBLE_CELSIUS < main["temp"] < MAX_PLAUSIBLE_CELSIUS
    assert main["temp_min"] <= main["temp"] <= main["temp_max"]


def test_observation_timestamp_is_recent(madrid_metric: requests.Response) -> None:
    observed_at = madrid_metric.json()["dt"]

    assert abs(time.time() - observed_at) < ONE_DAY_SECONDS


def test_imperial_temperature_is_consistent_with_metric(
    fetch: Fetch, madrid_metric: requests.Response
) -> None:
    imperial = fetch({"q": "Madrid", "units": "imperial"})
    celsius = madrid_metric.json()["main"]["temp"]
    fahrenheit = imperial.json()["main"]["temp"]

    assert imperial.status_code == 200
    assert fahrenheit == pytest.approx(celsius * 9 / 5 + 32, abs=3.0)


def test_coordinates_query_resolves_the_same_area_as_the_city_query(
    fetch: Fetch, madrid_metric: requests.Response
) -> None:
    coord = madrid_metric.json()["coord"]

    response = fetch({"lat": coord["lat"], "lon": coord["lon"], "units": "metric"})
    body = response.json()

    assert response.status_code == 200
    assert body["sys"]["country"] == "ES"
    assert body["coord"]["lat"] == pytest.approx(coord["lat"], abs=0.1)
    assert body["coord"]["lon"] == pytest.approx(coord["lon"], abs=0.1)


@pytest.mark.parametrize(
    "credentials",
    [{"send_key": False}, {"key": "invalid-key"}],
    ids=["missing-key", "invalid-key"],
)
def test_requests_without_a_valid_key_are_unauthorized(
    fetch: Fetch, credentials: dict[str, Any]
) -> None:
    response = fetch({"q": "Madrid"}, **credentials)

    assert response.status_code == 401
    assert int(response.json()["cod"]) == 401
    assert "api key" in response.json()["message"].lower()


def test_unknown_city_returns_not_found(fetch: Fetch) -> None:
    response = fetch({"q": "Zzzzqqxx"})

    assert response.status_code == 404
    assert int(response.json()["cod"]) == 404
    assert "not found" in response.json()["message"].lower()


def test_request_without_location_is_rejected(fetch: Fetch) -> None:
    response = fetch({})

    assert response.status_code == 400
    assert int(response.json()["cod"]) == 400
    assert response.json()["message"]


def test_out_of_range_latitude_is_rejected(fetch: Fetch) -> None:
    response = fetch({"lat": 999, "lon": 0})

    assert response.status_code == 400
    assert "latitude" in response.json()["message"].lower()


def test_client_returns_a_typed_result_from_the_real_api(settings: Settings, api_key: str) -> None:
    client = WeatherClient(
        api_key=api_key,
        base_url=settings.owm_base_url,
        timeout_seconds=settings.owm_timeout_seconds,
    )

    weather = client.current_by_city("Madrid")

    assert weather.name == "Madrid"
    assert weather.condition.main
