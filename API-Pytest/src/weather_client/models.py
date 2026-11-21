from pydantic import BaseModel, ConfigDict, Field


class _Model(BaseModel):
    model_config = ConfigDict(strict=True, extra="ignore", populate_by_name=True)


class Coordinates(_Model):
    lon: float
    lat: float


class Condition(_Model):
    id: int
    main: str
    description: str
    icon: str


class MainMetrics(_Model):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: float


class Wind(_Model):
    speed: float
    deg: float | None = None
    gust: float | None = None


class Clouds(_Model):
    all: float


class Precipitation(_Model):
    one_hour: float | None = Field(default=None, alias="1h")
    three_hours: float | None = Field(default=None, alias="3h")


class SystemInfo(_Model):
    country: str | None = None
    sunrise: int | None = None
    sunset: int | None = None


class CurrentWeather(_Model):
    id: int
    name: str
    coord: Coordinates
    weather: list[Condition] = Field(min_length=1)
    main: MainMetrics
    dt: int
    timezone: int
    wind: Wind | None = None
    clouds: Clouds | None = None
    rain: Precipitation | None = None
    snow: Precipitation | None = None
    visibility: int | None = None
    sys: SystemInfo | None = None

    @property
    def condition(self) -> Condition:
        return self.weather[0]
