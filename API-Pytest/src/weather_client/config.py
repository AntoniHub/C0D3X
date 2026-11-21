from urllib.parse import urlsplit

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_BASE_URL = "https://api.openweathermap.org/data/2.5"
MAX_TIMEOUT_SECONDS = 60.0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    owm_api_key: SecretStr | None = None
    owm_base_url: str = DEFAULT_BASE_URL
    owm_timeout_seconds: float = Field(
        default=10.0, gt=0, le=MAX_TIMEOUT_SECONDS, allow_inf_nan=False
    )

    @field_validator("owm_api_key", mode="before")
    @classmethod
    def blank_key_is_missing(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("owm_base_url")
    @classmethod
    def require_https(cls, value: str) -> str:
        parts = urlsplit(value)
        if parts.scheme != "https" or not parts.hostname:
            raise ValueError("owm_base_url must be an https URL with a host")
        return value.rstrip("/")
