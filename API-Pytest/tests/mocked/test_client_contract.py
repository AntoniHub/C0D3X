from typing import Any

import pytest
import responses
from jsonschema import Draft202012Validator

from weather_client import MalformedResponseError, WeatherClient


def test_sample_payload_conforms_to_the_published_schema(
    madrid_payload: dict[str, Any], current_weather_schema: dict[str, Any]
) -> None:
    Draft202012Validator(current_weather_schema).validate(madrid_payload)


def test_valid_payload_is_parsed_into_the_model(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
) -> None:
    http.add(responses.GET, weather_url, json=madrid_payload)

    weather = client.current_by_city("Madrid")

    assert weather.name == "Madrid"
    assert weather.sys is not None
    assert weather.sys.country == "ES"
    assert weather.main.temp == pytest.approx(19.23)
    assert weather.condition.main == "Clear"
    assert weather.wind is not None
    assert weather.wind.gust == pytest.approx(6.111)


@pytest.mark.parametrize("field", ["wind", "clouds", "rain", "snow", "sys", "visibility"])
def test_optional_sections_may_be_absent(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
    field: str,
) -> None:
    madrid_payload.pop(field, None)
    http.add(responses.GET, weather_url, json=madrid_payload)

    weather = client.current_by_city("Madrid")

    assert getattr(weather, field) is None


def test_precipitation_volumes_are_exposed(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
) -> None:
    madrid_payload["rain"] = {"1h": 2.5}
    madrid_payload["snow"] = {"3h": 1.25}
    http.add(responses.GET, weather_url, json=madrid_payload)

    weather = client.current_by_city("Madrid")

    assert weather.rain is not None
    assert weather.rain.one_hour == pytest.approx(2.5)
    assert weather.rain.three_hours is None
    assert weather.snow is not None
    assert weather.snow.three_hours == pytest.approx(1.25)


def test_integer_measurements_are_accepted_as_floats(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
) -> None:
    madrid_payload["main"]["temp"] = 20
    http.add(responses.GET, weather_url, json=madrid_payload)

    assert client.current_by_city("Madrid").main.temp == pytest.approx(20.0)


def test_unknown_fields_are_ignored(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
) -> None:
    madrid_payload["brand_new_field"] = {"nested": True}
    http.add(responses.GET, weather_url, json=madrid_payload)

    assert client.current_by_city("Madrid").id == 3117735


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda p: p.update(weather=[]), id="empty-weather-list"),
        pytest.param(lambda p: p.pop("weather"), id="missing-weather"),
        pytest.param(lambda p: p.pop("main"), id="missing-main"),
        pytest.param(lambda p: p.pop("coord"), id="missing-coord"),
        pytest.param(lambda p: p["main"].update(temp="warm"), id="non-numeric-temperature"),
        pytest.param(lambda p: p["main"].update(temp="12.5"), id="numeric-string-temperature"),
        pytest.param(lambda p: p["main"].update(temp=None), id="null-temperature"),
        pytest.param(lambda p: p.update(weather=[{"id": 800}]), id="incomplete-condition"),
    ],
)
def test_payloads_violating_the_contract_are_rejected(
    client: WeatherClient,
    http: responses.RequestsMock,
    weather_url: str,
    madrid_payload: dict[str, Any],
    mutate: Any,
) -> None:
    mutate(madrid_payload)
    http.add(responses.GET, weather_url, json=madrid_payload)

    with pytest.raises(MalformedResponseError):
        client.current_by_city("Madrid")


@pytest.mark.parametrize(
    "body",
    ["", "not json", "[]", "null", '"text"'],
    ids=["empty", "plain-text", "array", "null", "string"],
)
def test_bodies_that_are_not_json_objects_are_rejected(
    client: WeatherClient, http: responses.RequestsMock, weather_url: str, body: str
) -> None:
    http.add(responses.GET, weather_url, body=body, status=200)

    with pytest.raises(MalformedResponseError):
        client.current_by_city("Madrid")


def test_error_payload_served_with_a_success_status_is_rejected(
    client: WeatherClient, http: responses.RequestsMock, weather_url: str
) -> None:
    http.add(responses.GET, weather_url, json={"cod": "404", "message": "city not found"})

    with pytest.raises(MalformedResponseError):
        client.current_by_city("Madrid")
