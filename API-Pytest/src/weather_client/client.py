import time
from collections.abc import Callable, Mapping
from enum import StrEnum
from typing import Any

import requests
from pydantic import ValidationError

from weather_client.config import DEFAULT_BASE_URL
from weather_client.errors import (
    AuthenticationError,
    InvalidRequestError,
    LocationNotFoundError,
    MalformedResponseError,
    RateLimitError,
    UpstreamError,
    WeatherApiError,
)
from weather_client.models import CurrentWeather

MAX_RETRY_DELAY_SECONDS = 30.0
RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


class Units(StrEnum):
    STANDARD = "standard"
    METRIC = "metric"
    IMPERIAL = "imperial"


class WeatherClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout_seconds: float = 10.0,
        max_retries: int = 2,
        backoff_seconds: float = 0.5,
        session: requests.Session | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if not api_key:
            raise ValueError("api_key must not be empty")
        if max_retries < 0:
            raise ValueError("max_retries must not be negative")
        self._api_key = api_key
        self._url = f"{base_url.rstrip('/')}/weather"
        self._timeout = timeout_seconds
        self._max_retries = max_retries
        self._backoff = backoff_seconds
        self._session = session or requests.Session()
        self._sleep = sleep

    def current_by_city(
        self, city: str, units: Units = Units.METRIC, lang: str | None = None
    ) -> CurrentWeather:
        if not city.strip():
            raise ValueError("city must not be blank")
        return self._fetch({"q": city.strip()}, units, lang)

    def current_by_coordinates(
        self, lat: float, lon: float, units: Units = Units.METRIC, lang: str | None = None
    ) -> CurrentWeather:
        if not -90 <= lat <= 90:
            raise ValueError("lat must be between -90 and 90")
        if not -180 <= lon <= 180:
            raise ValueError("lon must be between -180 and 180")
        return self._fetch({"lat": lat, "lon": lon}, units, lang)

    def _fetch(
        self, location: Mapping[str, str | float], units: Units, lang: str | None
    ) -> CurrentWeather:
        params: dict[str, str | float] = {**location, "units": units.value}
        if lang:
            params["lang"] = lang
        payload = self._request(params)
        try:
            return CurrentWeather.model_validate(payload)
        except ValidationError as exc:
            raise MalformedResponseError(
                f"Response does not match the expected contract: {exc.error_count()} error(s)"
            ) from exc

    def _request(self, params: Mapping[str, str | float]) -> dict[str, Any]:
        query = {**params, "appid": self._api_key}
        attempt = 0
        while True:
            try:
                response = self._session.get(self._url, params=query, timeout=self._timeout)
            except (requests.ConnectionError, requests.Timeout) as exc:
                # The original exception embeds the request URL, which contains the API key.
                if attempt >= self._max_retries:
                    raise UpstreamError(f"Network failure: {type(exc).__name__}") from None
                self._sleep(self._delay(attempt, None))
                attempt += 1
                continue

            if response.status_code == requests.codes.ok:
                return self._decode(response)
            if response.status_code in RETRYABLE_STATUS_CODES and attempt < self._max_retries:
                self._sleep(self._delay(attempt, response))
                attempt += 1
                continue
            raise self._to_error(response)

    def _delay(self, attempt: int, response: requests.Response | None) -> float:
        if response is not None:
            retry_after = response.headers.get("Retry-After", "")
            if retry_after.isdigit():
                return min(float(retry_after), MAX_RETRY_DELAY_SECONDS)
        return min(self._backoff * 2.0**attempt, MAX_RETRY_DELAY_SECONDS)

    @staticmethod
    def _decode(response: requests.Response) -> dict[str, Any]:
        try:
            body = response.json()
        except ValueError:
            raise MalformedResponseError("Response body is not valid JSON") from None
        if not isinstance(body, dict):
            raise MalformedResponseError("Response body is not a JSON object")
        return body

    @staticmethod
    def _to_error(response: requests.Response) -> WeatherApiError:
        status = response.status_code
        try:
            body = response.json()
            message = str(body.get("message", "")) if isinstance(body, dict) else ""
        except ValueError:
            message = ""
        message = message or f"Unexpected response with status {status}"

        if status == requests.codes.bad_request:
            return InvalidRequestError(message, status)
        if status == requests.codes.unauthorized:
            return AuthenticationError(message, status)
        if status == requests.codes.not_found:
            return LocationNotFoundError(message, status)
        if status == requests.codes.too_many_requests:
            return RateLimitError(message, status)
        if status >= requests.codes.internal_server_error:
            return UpstreamError(message, status)
        return WeatherApiError(message, status)
