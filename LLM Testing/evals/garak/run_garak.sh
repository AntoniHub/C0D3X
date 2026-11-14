#!/usr/bin/env bash
# Run a short, fully offline Garak scan against one agent instance.
# Usage: evals/garak/run_garak.sh <port> <output-dir> [python-binary]
# Built by QA Engineer | Antonio Rodriguez Farias
set -euo pipefail
PORT="$1"
mkdir -p "$2"
OUT="$(cd "$2" && pwd)"  # garak resolves relative prefixes against its own data dir
PY="${3:-python}"
HERE="$(cd "$(dirname "$0")" && pwd)"

PROBES="promptinject.HijackHateHumans,promptinject.HijackKillHumans,promptinject.HijackLongPrompt,dan.Dan_11_0,dan.DUDE"

CONFIG="$(mktemp)"
sed "s/:8000/:${PORT}/" "$HERE/rest_config.json" > "$CONFIG"

"$PY" -m garak \
  --model_type rest \
  -G "$CONFIG" \
  --probes "$PROBES" \
  --generations 1 \
  --report_prefix "$OUT/run" > "$OUT/garak.log" 2>&1 || true

rm -f "$CONFIG" "$OUT/run.report.html"
test -s "$OUT/run.report.jsonl" || { echo "garak produced no report, see $OUT/garak.log"; tail -20 "$OUT/garak.log"; exit 1; }
python3 - "$OUT/run.report.jsonl" <<'PY'
import json, sys
for line in open(sys.argv[1], encoding="utf-8"):
    entry = json.loads(line)
    if entry.get("entry_type") == "eval":
        state = "PASS" if entry["passed"] == entry["total_evaluated"] else "FAIL"
        print(f'{state}  {entry["probe"]:<34} {entry["detector"]:<36} {entry["passed"]}/{entry["total_evaluated"]}')
PY

