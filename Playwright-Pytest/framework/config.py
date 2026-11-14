"""Settings come from the environment, never from test code."""
import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO_APP = ROOT / "demo-app" / "app.py"


@dataclass(frozen=True)
class Settings:
    #: Target under test. Empty means "start the bundled demo app on a free port".
    base_url: str = os.getenv("BASE_URL", "")
    user: str = os.getenv("DEMO_USER", "qa.demo")
    password: str = os.getenv("DEMO_PASSWORD", "demo-pass")
    #: Maximum time for web-first assertions, in milliseconds.
    expect_timeout_ms: int = int(os.getenv("EXPECT_TIMEOUT_MS", "5000"))


SETTINGS = Settings()
