import os
import re

REDACTED = "[REDACTED]"
SECRET_ENVIRONMENT_VARIABLES = ("OWM_API_KEY", "ANTHROPIC_API_KEY", "GITHUB_TOKEN")
MIN_SECRET_LENGTH = 8

_NAMES = r"(?:appid|api[_-]?key|apikey|key|token|access_token|password|passwd|secret|auth)"
_QUOTED_PAIR = re.compile(rf"""(?i)(["']?\b{_NAMES}\b["']?\s*[:=]\s*)(["'])[^"'\n]*\2""")
_QUERY_PARAMETER = re.compile(rf"(?i)\b({_NAMES})=([^&\s'\"]+)")
_COLON_PAIR = re.compile(rf"""(?i)\b({_NAMES})\s*:\s*[^\s"',}}]+""")
_SENSITIVE_HEADER = re.compile(
    r"(?i)\b(authorization|x-api-key|cookie|set-cookie)\s*[:=]\s*[^\r\n]+"
)
_BEARER_TOKEN = re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._~+/=-]{8,}")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_HEX_KEY = re.compile(r"(?i)\b[0-9a-f]{32}\b")
_TOKEN_FORMATS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{32,}"),
)


def _known_secrets() -> list[str]:
    values = (os.environ.get(name, "") for name in SECRET_ENVIRONMENT_VARIABLES)
    return [value for value in values if len(value) >= MIN_SECRET_LENGTH]


def redact(text: str) -> str:
    for secret in _known_secrets():
        text = text.replace(secret, REDACTED)
    text = _QUOTED_PAIR.sub(rf"\1\2{REDACTED}\2", text)
    text = _QUERY_PARAMETER.sub(rf"\1={REDACTED}", text)
    text = _COLON_PAIR.sub(rf"\1: {REDACTED}", text)
    text = _SENSITIVE_HEADER.sub(rf"\1: {REDACTED}", text)
    text = _BEARER_TOKEN.sub(rf"\1 {REDACTED}", text)
    for pattern in _TOKEN_FORMATS:
        text = pattern.sub(REDACTED, text)
    text = _HEX_KEY.sub(REDACTED, text)
    return _EMAIL.sub(REDACTED, text)
