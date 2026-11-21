from qa_triage.models import Failure, Triage

FINGERPRINT_MARKER = "qa-triage:fp="
NOT_TRIAGED = "not triaged"
MAX_MODEL_TEXT_CHARS = 500
_FENCE = "```"
_ZERO_WIDTH_SPACE = "​"


def render_issue(
    results: list[tuple[Failure, Triage | None]], fingerprint: str, total: int | None = None
) -> str:
    sections = [
        f"<!-- {FINGERPRINT_MARKER}{fingerprint} -->",
        "# Test failures triage",
        f"{_count_sentence(len(results), total)} Fingerprint `{fingerprint}`.",
        _summary_table(results),
    ]
    sections.extend(_failure_section(failure, triage) for failure, triage in results)
    return "\n\n".join(sections) + "\n"


def _count_sentence(shown: int, total: int | None) -> str:
    if total is None or total == shown:
        return f"{shown} failing test(s)."
    return f"Showing {shown} of {total} failing test(s)."


def _summary_table(results: list[tuple[Failure, Triage | None]]) -> str:
    rows = ["| Test | Category | Confidence |", "|---|---|---|"]
    for failure, triage in results:
        category = triage.category.value if triage else NOT_TRIAGED
        confidence = triage.confidence.value if triage else "-"
        rows.append(f"| `{_inline(failure.test_id)}` | {category} | {confidence} |")
    return "\n".join(rows)


def _failure_section(failure: Failure, triage: Triage | None) -> str:
    lines = [f"## `{_inline(failure.test_id)}`"]
    if triage:
        lines += [
            f"**Summary:** {_model_text(triage.summary)}",
            f"**Suspected cause:** {_model_text(triage.suspected_cause)}",
            f"**Next step:** {_model_text(triage.next_step)}",
        ]
    lines += [
        "<details><summary>Failure output (redacted)</summary>",
        f"{_FENCE}\n{_escape(failure.message)}\n{_escape(failure.details)}\n{_FENCE}",
        "</details>",
    ]
    return "\n\n".join(lines)


def _escape(text: str) -> str:
    return text.replace(_FENCE, "'''")


def _inline(text: str) -> str:
    return text.replace("|", "\\|").replace("`", "'")


def _model_text(text: str) -> str:
    cleaned = " ".join(text.split())[:MAX_MODEL_TEXT_CHARS]
    return cleaned.replace("<", "&lt;").replace("@", f"@{_ZERO_WIDTH_SPACE}")
