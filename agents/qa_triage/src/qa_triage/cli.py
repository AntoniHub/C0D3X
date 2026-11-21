import argparse
import os
import sys
from collections.abc import Callable
from pathlib import Path
from xml.etree.ElementTree import ParseError  # noqa: S405

import anthropic
from defusedxml import DefusedXmlException

from qa_triage.classifier import DEFAULT_MODEL, ModelClient, TriageError, Triager
from qa_triage.fingerprint import fingerprint
from qa_triage.junit import parse_failures
from qa_triage.models import Failure, Triage
from qa_triage.report import render_issue

API_KEY_VARIABLE = "ANTHROPIC_API_KEY"
MODEL_VARIABLE = "QA_TRIAGE_MODEL"
DEFAULT_MAX_FAILURES = 10
INPUT_ERROR_EXIT_CODE = 2
INPUT_ERRORS = (OSError, ParseError, DefusedXmlException)

Results = list[tuple[Failure, Triage | None]]


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="qa-triage", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    fingerprint_command = commands.add_parser("fingerprint", help="print the failure fingerprint")
    fingerprint_command.add_argument("junit", type=Path, nargs="+")

    triage_command = commands.add_parser("triage", help="classify failures and draft the issue")
    triage_command.add_argument("junit", type=Path, nargs="+")
    triage_command.add_argument("--out", type=Path, help="write the report here, default stdout")
    triage_command.add_argument("--dry-run", action="store_true", help="skip the model entirely")
    triage_command.add_argument("--max-failures", type=positive_int, default=DEFAULT_MAX_FAILURES)
    return parser


def classify_all(client: ModelClient, model: str, failures: list[Failure]) -> Results:
    triager = Triager(client, model)
    results: Results = []
    for failure in failures:
        try:
            results.append((failure, triager.classify(failure)))
        except (TriageError, anthropic.APIError) as exc:
            sys.stderr.write(f"Could not triage {failure.test_id}: {type(exc).__name__}\n")
            results.append((failure, None))
    return results


def load_failures(paths: list[Path]) -> list[Failure]:
    return [failure for path in paths for failure in parse_failures(path)]


def model_enabled(dry_run: bool) -> bool:
    if dry_run:
        return False
    if os.environ.get(API_KEY_VARIABLE):
        return True
    sys.stderr.write(f"{API_KEY_VARIABLE} is not set; the model was not called.\n")
    return False


def triage_results(
    selected: list[Failure], use_model: bool, client_factory: Callable[[], ModelClient]
) -> Results:
    if not use_model:
        return [(failure, None) for failure in selected]
    model = os.environ.get(MODEL_VARIABLE, DEFAULT_MODEL)
    return classify_all(client_factory(), model, selected)


def write_report(report: str, destination: Path | None) -> None:
    if destination:
        destination.write_text(report, encoding="utf-8")
    else:
        sys.stdout.write(report)


def run_triage(args: argparse.Namespace) -> int:
    failures = load_failures(args.junit)
    if not failures:
        sys.stderr.write("No failures found.\n")
        return 0

    selected = failures[: args.max_failures]
    results = triage_results(selected, model_enabled(args.dry_run), anthropic.Anthropic)
    write_report(render_issue(results, fingerprint(failures), len(failures)), args.out)
    return 0


def run_fingerprint(args: argparse.Namespace) -> int:
    failures = load_failures(args.junit)
    sys.stdout.write(fingerprint(failures) if failures else "none")
    sys.stdout.write("\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    handlers = {"triage": run_triage, "fingerprint": run_fingerprint}
    try:
        return handlers[args.command](args)
    except INPUT_ERRORS as exc:
        sys.stderr.write(f"Could not process the reports: {type(exc).__name__}\n")
        return INPUT_ERROR_EXIT_CODE
