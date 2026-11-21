from collections.abc import Callable, Iterator, Mapping

import pytest
import requests

from weather_client import Settings

Params = Mapping[str, str | float]
Fetch = Callable[..., requests.Response]


class LiveRequestError(RuntimeError):
    """Live call failed; the original error is dropped because it embeds the API key."""


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def api_key(settings: Settings) -> str:
    if settings.owm_api_key is None:
        pytest.skip("OWM_API_KEY is not configured")
    return settings.owm_api_key.get_secret_value()


@pytest.fixture(scope="session")
def http_session() -> Iterator[requests.Session]:
    with requests.Session() as session:
        yield session


@pytest.fixture(scope="session")
def fetch(settings: Settings, api_key: str, http_session: requests.Session) -> Fetch:
    url = f"{settings.owm_base_url}/weather"

    def call(params: Params, *, send_key: bool = True, key: str | None = None) -> requests.Response:
        query = dict(params)
        if send_key:
            query["appid"] = key if key is not None else api_key
        try:
            return http_session.get(url, params=query, timeout=settings.owm_timeout_seconds)
        except requests.RequestException as exc:
            raise LiveRequestError(f"Live request failed: {type(exc).__name__}") from None

    return call


@pytest.fixture(scope="session")
def madrid_metric(fetch: Fetch) -> requests.Response:
    return fetch({"q": "Madrid", "units": "metric"})
