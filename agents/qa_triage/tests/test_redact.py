import pytest

from qa_triage.redact import REDACTED, redact
from tests.fakes import FAKE_KEY_VALUE

AWS_KEY = "AKIA" + "B" * 16
GITHUB_TOKEN = "ghp_" + "c" * 36
ANTHROPIC_KEY = "sk-ant-" + "d" * 24


@pytest.mark.parametrize(
    "text",
    [
        f"GET /weather?q=Madrid&appid={FAKE_KEY_VALUE} failed",
        f"https://api.example.com/v1?api_key={FAKE_KEY_VALUE}",
        f"token={FAKE_KEY_VALUE}&other=1",
        f"Authorization: Bearer {FAKE_KEY_VALUE}",
        f"x-api-key: {FAKE_KEY_VALUE}",
        f"Cookie: session={FAKE_KEY_VALUE}",
        f"leaked {AWS_KEY} here",
        f"leaked {GITHUB_TOKEN} here",
        f"leaked {ANTHROPIC_KEY} here",
        f'{{"token": "{FAKE_KEY_VALUE}"}}',
        f"password: {FAKE_KEY_VALUE}",
        f"api_key: '{FAKE_KEY_VALUE}'",
    ],
)
def test_secrets_are_removed(text: str) -> None:
    cleaned = redact(text)

    assert REDACTED in cleaned
    for secret in (FAKE_KEY_VALUE, AWS_KEY, GITHUB_TOKEN, ANTHROPIC_KEY):
        assert secret not in cleaned


def test_unlabelled_hex_keys_are_removed() -> None:
    hex_key = "0123456789abcdef" * 2

    assert hex_key not in redact(f"the provider rejected {hex_key} as invalid")


def test_values_of_known_environment_secrets_are_removed(monkeypatch: pytest.MonkeyPatch) -> None:
    leaked_value = "an-unlabelled-value-1234"
    monkeypatch.setenv("ANTHROPIC_API_KEY", leaked_value)

    assert leaked_value not in redact(f"assertion failed for {leaked_value}")


def test_emails_are_removed() -> None:
    assert "person@example.com" not in redact("user person@example.com logged in")


def test_surrounding_text_is_kept() -> None:
    cleaned = redact(f"GET /weather?q=Madrid&appid={FAKE_KEY_VALUE} returned 401")

    assert cleaned.startswith("GET /weather?q=Madrid&appid=")
    assert cleaned.endswith("returned 401")


@pytest.mark.parametrize("text", ["assert 1 == 2", "TimeoutError after 10 s", "monkey=banana"])
def test_ordinary_text_is_unchanged(text: str) -> None:
    assert redact(text) == text
