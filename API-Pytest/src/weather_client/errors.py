class WeatherApiError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class InvalidRequestError(WeatherApiError):
    pass


class AuthenticationError(WeatherApiError):
    pass


class LocationNotFoundError(WeatherApiError):
    pass


class RateLimitError(WeatherApiError):
    pass


class UpstreamError(WeatherApiError):
    pass


class MalformedResponseError(WeatherApiError):
    pass
