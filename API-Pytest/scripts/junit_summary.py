import argparse
import sys
import xml.etree.ElementTree as ET  # noqa: S405
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Totals:
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    seconds: float = 0.0
    failures: list[str] = field(default_factory=list)
    skips: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.passed + self.failed + self.skipped


def read_totals(path: Path) -> Totals:
    totals = Totals()
    # The file is produced by the test runners of this same job, not by an external party.
    root = ET.parse(path).getroot()  # noqa: S314
    for case in root.iter("testcase"):
        name = f"{case.get('classname', '')}::{case.get('name', '')}".strip(":")
        totals.seconds += float(case.get("time", "0") or 0)
        if case.find("failure") is not None or case.find("error") is not None:
            totals.failed += 1
            totals.failures.append(name)
        elif (skipped := case.find("skipped")) is not None:
            totals.skipped += 1
            reason = skipped.get("message", "").strip()
            totals.skips.append(f"{name} ({reason})" if reason else name)
        else:
            totals.passed += 1
    return totals


def render(title: str, totals: Totals) -> str:
    outcome = "failed" if totals.failed else "passed"
    lines = [
        f"### {title}: {outcome}",
        "",
        "| Total | Passed | Failed | Skipped | Duration |",
        "| ---: | ---: | ---: | ---: | ---: |",
        f"| {totals.total} | {totals.passed} | {totals.failed} | {totals.skipped} "
        f"| {totals.seconds:.1f} s |",
    ]
    if totals.failures:
        lines += ["", "Failed tests:", *(f"- `{name}`" for name in totals.failures)]
    if totals.skips:
        lines += ["", "Skipped tests:", *(f"- `{name}`" for name in totals.skips)]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render a JUnit XML file as a Markdown summary.")
    parser.add_argument("title")
    parser.add_argument("junit_file", type=Path)
    args = parser.parse_args(argv)

    if not args.junit_file.is_file():
        sys.stdout.write(f"### {args.title}\n\nNo results file was produced.\n")
        return 0
    sys.stdout.write(render(args.title, read_totals(args.junit_file)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
