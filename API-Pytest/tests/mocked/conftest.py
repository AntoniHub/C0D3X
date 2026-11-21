from collections.abc import Callable, Iterator
from urllib.parse import parse_qsl, urlparse

import pytest
import responses

from weather_client import WeatherClient

BASE_URL = "https://weather.test/data/2.5"


class SleepRecorder:
    def __init__(self) -> None:
        self.delays: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.delays.append(seconds)


@pytest.fixture
def weather_url() -> str:
    return f"{BASE_URL}/weather"


@pytest.fixture
def http() -> Iterator[responses.RequestsMock]:
    with responses.RequestsMock() as mock:
        yield mock


@pytest.fixture
def sleeper() -> SleepRecorder:
    return SleepRecorder()


@pytest.fixture
def client(sleeper: SleepRecorder) -> WeatherClient:
    return WeatherClient(
        api_key="test-key",
        base_url=BASE_URL,
        max_retries=2,
        backoff_seconds=0.5,
        sleep=sleeper,
    )


@pytest.fixture
def last_query(http: responses.RequestsMock) -> Callable[[], dict[str, str]]:
    def read() -> dict[str, str]:
        url = http.calls[-1].request.url
        assert url is not None
        return dict(parse_qsl(urlparse(url).query))

    return read
