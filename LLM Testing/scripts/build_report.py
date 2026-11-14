#!/usr/bin/env python3
"""Turn the raw output of every eval tool into one HTML report plus a short summary.

Inputs (all under --raw):
    unit.xml                      pytest JUnit output for the agent unit tests
    deepeval.jsonl                one row per golden case
    promptfoo.json                Promptfoo --output file
    garak/*.report.jsonl          Garak report files
    canary/...                    the same files, produced against the vulnerable variant

The canary results are expected to FAIL. If a tool does not catch the vulnerable agent,
the tool itself is broken, so that counts against the run.

Built by QA Engineer | Antonio Rodriguez Farias
"""
import argparse
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNATURE = "QA Engineer | Antonio Rodriguez Farias"
HISTORY_LIMIT = 90


# ----------------------------------------------------------------------------- loading
def load_unit(raw: Path) -> dict:
    path = raw / "unit.xml"
    if not path.exists():
        return {"total": 0, "passed": 0, "rows": [], "missing": True}
    root = ET.parse(path).getroot()
    rows = []
    for case in root.iter("testcase"):
        failed = case.find("failure") is not None or case.find("error") is not None
        skipped = case.find("skipped") is not None
        rows.append({"name": f"{case.get('classname', '').split('.')[-1]}::{case.get('name')}", "passed": not failed and not skipped})
    passed = sum(1 for r in rows if r["passed"])
    return {"total": len(rows), "passed": passed, "rows": rows}


def load_deepeval(raw: Path) -> dict:
    path = raw / "deepeval.jsonl"
    if not path.exists():
        return {"total": 0, "passed": 0, "rows": [], "missing": True}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {"total": len(rows), "passed": sum(1 for r in rows if r["passed"]), "rows": rows}


def load_promptfoo(raw: Path) -> dict:
    path = raw / "promptfoo.json"
    if not path.exists():
        return {"total": 0, "passed": 0, "rows": [], "missing": True}
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for item in data["results"]["results"]:
        grading = item.get("gradingResult") or {}
        failures = [
            c.get("reason", "")
            for c in grading.get("componentResults", [])
            if not c.get("pass", True)
        ]
        rows.append(
            {
                "name": (item.get("testCase") or {}).get("description", "case"),
                "category": ((item.get("testCase") or {}).get("metadata") or {}).get("category", ""),
                "passed": bool(item.get("success")),
                "latency_ms": item.get("latencyMs"),
                "output": (item.get("response") or {}).get("output", ""),
                "reason": "; ".join(failures),
            }
        )
    return {"total": len(rows), "passed": sum(1 for r in rows if r["passed"]), "rows": rows}


def load_garak(raw: Path) -> dict:
    files = sorted((raw / "garak").glob("*.report.jsonl")) if (raw / "garak").exists() else []
    if not files:
        return {"total": 0, "passed": 0, "rows": [], "missing": True}
    rows = []
    for file in files:
        for line in file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            entry = json.loads(line)
            if entry.get("entry_type") != "eval":
                continue
            total = entry.get("total", entry.get("total_evaluated", 0)) or 0
            passed = entry.get("passed", entry.get("total_processed", 0) - entry.get("fails", 0))
            rows.append(
                {
                    "name": entry.get("probe", "probe"),
                    "detector": entry.get("detector", ""),
                    "passed_n": passed,
                    "total_n": total,
                    "passed": total > 0 and passed == total,
                }
            )
    return {"total": len(rows), "passed": sum(1 for r in rows if r["passed"]), "rows": rows}


def load_all(raw: Path) -> dict:
    return {
        "unit": load_unit(raw),
        "deepeval": load_deepeval(raw),
        "promptfoo": load_promptfoo(raw),
        "garak": load_garak(raw),
    }


# ----------------------------------------------------------------------------- judgement
def judge(main: dict, canary: dict) -> dict:
    suites_ok = {
        name: (not main[name].get("missing")) and main[name]["total"] > 0 and main[name]["passed"] == main[name]["total"]
        for name in main
    }
    detection = {}
    for name in ("deepeval", "promptfoo", "garak"):
        data = canary.get(name, {"total": 0, "passed": 0, "missing": True})
        failed = data["total"] - data["passed"]
        detection[name] = {
            "total": data["total"],
            "failed": failed,
            "detected": (not data.get("missing")) and failed > 0,
            "missing": bool(data.get("missing")),
        }
    detection_ok = all(d["detected"] for d in detection.values())
    return {
        "suites_ok": suites_ok,
        "detection": detection,
        "detection_ok": detection_ok,
        "status": "PASS" if all(suites_ok.values()) and detection_ok else "FAIL",
    }


# ----------------------------------------------------------------------------- context
def run_context() -> dict:
    repo = os.getenv("GITHUB_REPOSITORY", "")
    run_id = os.getenv("GITHUB_RUN_ID", "")
    server = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "day": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "trigger": os.getenv("GITHUB_EVENT_NAME", "local"),
        "branch": os.getenv("GITHUB_REF_NAME", "local"),
        "sha": os.getenv("GITHUB_SHA", "local")[:7],
        "run_id": run_id,
        "run_url": f"{server}/{repo}/actions/runs/{run_id}" if repo and run_id else "",
    }


# ----------------------------------------------------------------------------- html helpers
e = html.escape
CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#1c2330;--muted:#5d6878;--line:#e2e6ec;--pass:#1a7f4b;--passbg:#e5f5ec;--fail:#c0392b;--failbg:#fbe9e7;--accent:#2457c5}
@media (prefers-color-scheme:dark){:root{--bg:#0f1319;--card:#171d26;--ink:#e6eaf0;--muted:#95a0b0;--line:#283140;--pass:#4cc38a;--passbg:#14301f;--fail:#ff7b6b;--failbg:#381a17;--accent:#7aa2ff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1120px;margin:0 auto;padding:28px 16px 60px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:18px;margin:34px 0 10px}
.sub{color:var(--muted);margin:0 0 18px}.meta{display:flex;flex-wrap:wrap;gap:6px 18px;color:var(--muted);font-size:13px;margin-bottom:18px}
.meta b{color:var(--ink);font-weight:600}
.banner{border-radius:10px;padding:14px 18px;font-weight:600;margin:14px 0 20px}
.banner.pass{background:var(--passbg);color:var(--pass)}.banner.fail{background:var(--failbg);color:var(--fail)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card .k{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.card .v{font-size:26px;font-weight:700;margin-top:2px}.card .s{font-size:13px;color:var(--muted)}
.card.pass .v{color:var(--pass)}.card.fail .v{color:var(--fail)}
.bar{height:6px;border-radius:3px;background:var(--line);margin-top:8px;overflow:hidden}.bar i{display:block;height:100%;background:var(--pass)}
.card.fail .bar i{background:var(--fail)}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:14px}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);background:var(--bg)}
tr:last-child td{border-bottom:none}.wrap{overflow-x:auto}
.pill{display:inline-block;padding:1px 9px;border-radius:99px;font-size:12px;font-weight:600}
.pill.pass{background:var(--passbg);color:var(--pass)}.pill.fail{background:var(--failbg);color:var(--fail)}
.chip{display:inline-block;margin:0 4px 3px 0;padding:0 7px;border:1px solid var(--line);border-radius:6px;font-size:12px}
.chip.fail{border-color:var(--fail);color:var(--fail)}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px}
details summary{cursor:pointer;color:var(--accent)}pre{white-space:pre-wrap;margin:6px 0 0;color:var(--muted)}
.note{color:var(--muted);font-size:13px;margin:6px 0 0}
footer{margin-top:40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:14px}
"""


def pill(ok: bool, yes: str = "PASS", no: str = "FAIL") -> str:
    return f'<span class="pill {"pass" if ok else "fail"}">{yes if ok else no}</span>'


def pct(passed: int, total: int) -> int:
    return round(100 * passed / total) if total else 0


def card(label: str, passed: int, total: int, ok: bool, noun: str = "passed") -> str:
    cls = "pass" if ok else "fail"
    return (
        f'<div class="card {cls}"><div class="k">{e(label)}</div><div class="v">{passed}/{total}</div>'
        f'<div class="s">{pct(passed, total)}% {noun}</div><div class="bar"><i style="width:{pct(passed, total)}%"></i></div></div>'
    )


def trunc(text: str, limit: int = 400) -> str:
    text = str(text)
    return text if len(text) <= limit else text[: limit - 1] + "..."


# ----------------------------------------------------------------------------- html sections
def section_deepeval(data: dict) -> str:
    rows = []
    for r in data["rows"]:
        chips = "".join(
            f'<span class="chip {"" if m["passed"] else "fail"}" title="{e(m["reason"])}">{e(m["name"])} {"" if m["score"] is None else m["score"]}</span>'
            for m in r["metrics"]
        )
        tools = ", ".join(r["tools_called"]) or "none"
        rows.append(
            f'<tr><td><b>{e(r["id"])}</b><br><span class="note">{e(trunc(r["input"], 90))}</span></td><td>{e(r["category"])}</td>'
            f'<td>{pill(r["passed"])}</td><td>{chips}</td><td><code>{e(tools)}</code></td>'
            f'<td>{r["latency_ms"]} ms</td><td><details><summary>view</summary><pre>{e(trunc(r["output"]))}</pre></details></td></tr>'
        )
    return (
        '<h2>DeepEval: quality, safety and grounding</h2><div class="wrap"><table><tr><th>Case</th><th>Category</th><th>Result</th>'
        "<th>Metrics</th><th>Tools called</th><th>Latency</th><th>Output</th></tr>" + "".join(rows) + "</table></div>"
    )


def section_promptfoo(data: dict) -> str:
    rows = []
    for r in data["rows"]:
        reason = f'<span class="note">{e(trunc(r["reason"], 160))}</span>' if r["reason"] else ""
        rows.append(
            f'<tr><td><b>{e(r["name"])}</b>{("<br>" + reason) if reason else ""}</td><td>{e(r["category"])}</td><td>{pill(r["passed"])}</td>'
            f'<td>{r["latency_ms"]} ms</td><td><details><summary>view</summary><pre>{e(trunc(r["output"]))}</pre></details></td></tr>'
        )
    return (
        '<h2>Promptfoo: regression and adversarial checks</h2><div class="wrap"><table><tr><th>Test</th><th>Category</th><th>Result</th>'
        "<th>Latency</th><th>Output</th></tr>" + "".join(rows) + "</table></div>"
    )


def section_garak(data: dict) -> str:
    rows = "".join(
        f'<tr><td><code>{e(r["name"])}</code></td><td><code>{e(r["detector"])}</code></td><td>{r["passed_n"]}/{r["total_n"]}</td>'
        f'<td>{pill(r["passed"])}</td></tr>'
        for r in data["rows"]
    )
    return (
        '<h2>Garak: vulnerability scan</h2><div class="wrap"><table><tr><th>Probe</th><th>Detector</th><th>Prompts handled safely</th>'
        f"<th>Result</th></tr>{rows}</table></div>"
    )


def section_detection(verdict: dict, canary: dict) -> str:
    rows = []
    for name, d in verdict["detection"].items():
        failed_names = []
        if name == "deepeval":
            failed_names = [r["id"] for r in canary["deepeval"]["rows"] if not r["passed"]]
        elif name == "promptfoo":
            failed_names = [r["name"] for r in canary["promptfoo"]["rows"] if not r["passed"]]
        elif name == "garak":
            failed_names = [f'{r["name"]} / {r["detector"]}' for r in canary["garak"]["rows"] if not r["passed"]]
        listing = "<br>".join(e(n) for n in failed_names) or "-"
        rows.append(
            f'<tr><td><b>{e(name)}</b></td><td>{d["total"]}</td><td>{d["failed"]}</td>'
            f'<td>{pill(d["detected"], "CAUGHT", "MISSED")}</td><td><details><summary>list</summary><div class="note">{listing}</div></details></td></tr>'
        )
    return (
        "<h2>Detection check: does the suite catch a broken agent?</h2>"
        '<p class="note">The same tools run against a deliberately vulnerable variant of the agent (no guardrails, no ownership check). '
        "Failures are expected here. If a tool reports zero failures, the tool is not doing its job.</p>"
        '<div class="wrap"><table><tr><th>Tool</th><th>Checks</th><th>Failed on vulnerable agent</th><th>Verdict</th><th>Failed checks</th></tr>'
        + "".join(rows)
        + "</table></div>"
    )


def section_history(history: list) -> str:
    if not history:
        return ""

    def cell(s):
        return f'{s[0]}/{s[1]}'

    rows = "".join(
        f'<tr><td>{e(h["date"])}</td><td>{e(h["trigger"])}</td><td><code>{e(h["sha"])}</code></td><td>{cell(h["suites"]["unit"])}</td>'
        f'<td>{cell(h["suites"]["deepeval"])}</td><td>{cell(h["suites"]["promptfoo"])}</td><td>{cell(h["suites"]["garak"])}</td>'
        f'<td>{pill(h["detection_ok"], "CAUGHT", "MISSED")}</td><td>{pill(h["status"] == "PASS")}</td></tr>'
        for h in reversed(history[-14:])
    )
    return (
        "<h2>Run history</h2><div class=\"wrap\"><table><tr><th>Date</th><th>Trigger</th><th>Commit</th><th>Unit</th><th>DeepEval</th>"
        f"<th>Promptfoo</th><th>Garak</th><th>Detection</th><th>Status</th></tr>{rows}</table></div>"
    )


def render_html(main: dict, canary: dict, verdict: dict, ctx: dict, history: list) -> str:
    ok = verdict["status"] == "PASS"
    cards = "".join(
        card(label, main[key]["passed"], main[key]["total"], verdict["suites_ok"][key])
        for label, key in (("Unit tests", "unit"), ("DeepEval", "deepeval"), ("Promptfoo", "promptfoo"), ("Garak", "garak"))
    )
    caught = sum(1 for d in verdict["detection"].values() if d["detected"])
    cards += card("Detection check", caught, 3, verdict["detection_ok"], "tools caught the broken agent")
    link = f'<a href="{e(ctx["run_url"])}">run #{e(ctx["run_id"])}</a>' if ctx["run_url"] else "local run"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LLM Testing Report</title><style>{CSS}</style></head><body><main>
<h1>LLM Testing Report</h1>
<p class="sub">Automated evaluation of the Shopwise support agent (LangChain + LangGraph, mock model) with DeepEval, Promptfoo and Garak.</p>
<div class="meta"><span>Generated <b>{e(ctx["date"])}</b></span><span>Trigger <b>{e(ctx["trigger"])}</b></span><span>Branch <b>{e(ctx["branch"])}</b></span>
<span>Commit <b>{e(ctx["sha"])}</b></span><span>{link}</span></div>
<div class="banner {"pass" if ok else "fail"}">{"All suites passed on the hardened agent and every tool caught the vulnerable one." if ok else "This run needs attention: at least one suite failed or a tool missed the vulnerable agent."}</div>
<div class="cards">{cards}</div>
{section_detection(verdict, canary)}
{section_deepeval(main["deepeval"])}
{section_promptfoo(main["promptfoo"])}
{section_garak(main["garak"])}
{section_history(history)}
<footer>Built by {e(SIGNATURE)}. Agent model: scripted mock (see README for what that does and does not prove).</footer>
</main></body></html>"""


def render_summary(main: dict, verdict: dict, ctx: dict) -> str:
    def row(label, key):
        d = main[key]
        return f"| {label} | {d['passed']}/{d['total']} | {pct(d['passed'], d['total'])}% | {'PASS' if verdict['suites_ok'][key] else 'FAIL'} |"

    lines = [
        f"### LLM Testing: {verdict['status']}",
        "",
        f"Run: {ctx['date']} | trigger: {ctx['trigger']} | commit: `{ctx['sha']}`",
        "",
        "| Suite (hardened agent) | Passed | Rate | Result |",
        "|---|---|---|---|",
        row("Unit tests", "unit"),
        row("DeepEval", "deepeval"),
        row("Promptfoo", "promptfoo"),
        row("Garak", "garak"),
        "",
        "| Detection check (vulnerable agent) | Checks | Failed | Verdict |",
        "|---|---|---|---|",
    ]
    for name, d in verdict["detection"].items():
        lines.append(f"| {name} | {d['total']} | {d['failed']} | {'CAUGHT' if d['detected'] else 'MISSED'} |")
    lines += ["", f"_{SIGNATURE}_", ""]
    return "\n".join(lines)


def update_readme(readme: Path, summary_table: str) -> None:
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    pattern = re.compile(r"(<!-- LATEST-RUN:START -->).*?(<!-- LATEST-RUN:END -->)", re.S)
    if pattern.search(text):
        readme.write_text(pattern.sub(lambda m: f"{m.group(1)}\n{summary_table}\n{m.group(2)}", text), encoding="utf-8")


# ----------------------------------------------------------------------------- main
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default=str(ROOT / "reports" / "raw"))
    parser.add_argument("--out", default=str(ROOT / "reports" / "latest"))
    parser.add_argument("--history", default=str(ROOT / "reports" / "history.json"))
    parser.add_argument("--archive", default=str(ROOT / "reports" / "archive"))
    parser.add_argument("--record-history", action="store_true", help="append this run to history and archive the HTML")
    parser.add_argument("--update-readme", action="store_true")
    parser.add_argument("--fail-on-red", action="store_true")
    args = parser.parse_args()

    raw = Path(args.raw)
    main_data = load_all(raw)
    canary_data = load_all(raw / "canary")
    verdict = judge(main_data, canary_data)
    ctx = run_context()

    history_path = Path(args.history)
    history = json.loads(history_path.read_text()) if history_path.exists() else []
    entry = {
        "date": ctx["date"],
        "day": ctx["day"],
        "trigger": ctx["trigger"],
        "sha": ctx["sha"],
        "status": verdict["status"],
        "detection_ok": verdict["detection_ok"],
        "suites": {k: [main_data[k]["passed"], main_data[k]["total"]] for k in main_data},
    }
    shown_history = history + [entry]

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    page = render_html(main_data, canary_data, verdict, ctx, shown_history)
    (out / "index.html").write_text(page, encoding="utf-8")
    summary = render_summary(main_data, verdict, ctx)
    (out / "summary.md").write_text(summary, encoding="utf-8")
    (out / "summary.json").write_text(json.dumps({"context": ctx, "verdict": verdict, "entry": entry}, indent=2), encoding="utf-8")

    if args.record_history:
        history_path.parent.mkdir(parents=True, exist_ok=True)
        history_path.write_text(json.dumps((history + [entry])[-HISTORY_LIMIT:], indent=2), encoding="utf-8")
        archive = Path(args.archive)
        archive.mkdir(parents=True, exist_ok=True)
        (archive / f"{ctx['day']}.html").write_text(page, encoding="utf-8")
    if args.update_readme:
        update_readme(ROOT / "README.md", summary.split("\n_")[0].strip())

    print(summary)
    return 1 if (args.fail_on_red and verdict["status"] != "PASS") else 0


if __name__ == "__main__":
    sys.exit(main())

