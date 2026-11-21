import hashlib
import re

from qa_triage.models import Failure

_NUMBERS = re.compile(r"\d+")
FINGERPRINT_LENGTH = 12


def fingerprint(failures: list[Failure]) -> str:
    parts = sorted(f"{f.test_id}|{_NUMBERS.sub('N', f.message)}" for f in failures)
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    return digest[:FINGERPRINT_LENGTH]
