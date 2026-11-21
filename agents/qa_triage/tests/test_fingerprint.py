from qa_triage.fingerprint import FINGERPRINT_LENGTH, fingerprint
from qa_triage.models import Failure


def failure(test_id: str = "t::a", message: str = "timeout after 10 s") -> Failure:
    return Failure(test_id=test_id, message=message, details="")


def test_fingerprint_has_a_fixed_length() -> None:
    assert len(fingerprint([failure()])) == FINGERPRINT_LENGTH


def test_order_does_not_matter() -> None:
    first, second = failure("t::a"), failure("t::b")

    assert fingerprint([first, second]) == fingerprint([second, first])


def test_changing_numbers_do_not_change_the_fingerprint() -> None:
    assert fingerprint([failure(message="timeout after 10 s")]) == fingerprint(
        [failure(message="timeout after 12 s")]
    )


def test_a_different_test_changes_the_fingerprint() -> None:
    assert fingerprint([failure("t::a")]) != fingerprint([failure("t::b")])


def test_a_different_message_changes_the_fingerprint() -> None:
    assert fingerprint([failure(message="timeout")]) != fingerprint([failure(message="refused")])
