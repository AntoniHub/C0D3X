"""Single place for every setting. Values come from the environment, never from test code."""
import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO_APP = ROOT / "demo-app" / "app.py"


@dataclass(frozen=True)
class Settings:
    #: Target under test. Empty means "start the bundled demo app on a free port".
    base_url: str = os.getenv("BASE_URL", "")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = os.getenv("HEADLESS", "1") not in ("0", "false", "False")
    #: Maximum wait for any explicit wait, in seconds.
    timeout: int = int(os.getenv("UI_TIMEOUT", "10"))
    user: str = os.getenv("DEMO_USER", "qa.demo")
    password: str = os.getenv("DEMO_PASSWORD", "demo-pass")


SETTINGS = Settings()
