"""Append eval results to a JSONL file that the report builder reads later."""
import json
import os
from pathlib import Path

DEFAULT_DIR = Path(__file__).resolve().parents[2] / "reports" / "raw"


def results_dir() -> Path:
    path = Path(os.getenv("EVAL_RESULTS_DIR", DEFAULT_DIR))
    path.mkdir(parents=True, exist_ok=True)
    return path


def record(suite: str, row: dict) -> None:
    with open(results_dir() / f"{suite}.jsonl", "a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")

