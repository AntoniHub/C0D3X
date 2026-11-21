from collections.abc import Callable
from typing import Any

import pytest
import responses

from weather_client import Units, WeatherClient


def test_city_request_defaults_to_metric_units(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
    last_query: Callable[[], dict[str, str]],
) -> None:
    http.add(responses.GET, weather_url, json=madrid_payload)

    client.current_by_city("Madrid")

    assert last_query() == {"q": "Madrid", "units": "metric", "appid": "test-key"}


def test_city_request_forwards_units_and_language(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
    last_query: Callable[[], dict[str, str]],
) -> None:
    http.add(responses.GET, weather_url, json=madrid_payload)

    client.current_by_city("Madrid", units=Units.IMPERIAL, lang="es")

    assert last_query() == {"q": "Madrid", "units": "imperial", "lang": "es", "appid": "test-key"}


def test_city_name_is_trimmed_before_sending(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
    last_query: Callable[[], dict[str, str]],
) -> None:
    http.add(responses.GET, weather_url, json=madrid_payload)

    client.current_by_city("  Madrid  ")

    assert last_query()["q"] == "Madrid"


def test_coordinates_request_sends_lat_and_lon(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
    last_query: Callable[[], dict[str, str]],
) -> None:
    http.add(responses.GET, weather_url, json=madrid_payload)

    client.current_by_coordinates(40.4165, -3.7026, units=Units.STANDARD)

    assert last_query() == {
        "lat": "40.4165",
        "lon": "-3.7026",
        "units": "standard",
        "appid": "test-key",
    }


def test_trailing_slash_in_base_url_is_tolerated(
    http: responses.RequestsMock, weather_url: str, madrid_payload: dict[str, Any]
) -> None:
    http.add(responses.GET, weather_url, json=madrid_payload)
    client = WeatherClient(api_key="test-key", base_url="https://weather.test/data/2.5/")

    assert client.current_by_city("Madrid").name == "Madrid"


@pytest.mark.parametrize("city", ["", "   "])
def test_blank_city_is_rejected_without_calling_the_api(
    client: WeatherClient, http: responses.RequestsMock, city: str
) -> None:
    with pytest.raises(ValueError, match="city"):
        client.current_by_city(city)

    assert len(http.calls) == 0


@pytest.mark.parametrize(
    ("lat", "lon", "field"),
    [(90.1, 0.0, "lat"), (-90.1, 0.0, "lat"), (0.0, 180.1, "lon"), (0.0, -180.1, "lon")],
)
def test_out_of_range_coordinates_are_rejected_without_calling_the_api(
    client: WeatherClient, http: responses.RequestsMock, lat: float, lon: float, field: str
) -> None:
    with pytest.raises(ValueError, match=field):
        client.current_by_coordinates(lat, lon)

    assert len(http.calls) == 0


@pytest.mark.parametrize(("lat", "lon"), [(90.0, 180.0), (-90.0, -180.0), (0.0, 0.0)])
def test_boundary_coordinates_are_accepted(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
    lat: float,
    lon: float,
) -> None:
    http.add(responses.GET, weather_url, json=madrid_payload)

    client.current_by_coordinates(lat, lon)

    assert len(http.calls) == 1


def test_empty_api_key_is_rejected() -> None:
    with pytest.raises(ValueError, match="api_key"):
        WeatherClient(api_key="")


def test_negative_retry_count_is_rejected() -> None:
    with pytest.raises(ValueError, match="max_retries"):
        WeatherClient(api_key="test-key", max_retries=-1)
