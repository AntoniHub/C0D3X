#!/usr/bin/env bash
# Run the whole battery locally and build the HTML report.
# Usage: scripts/run_all.sh [python-binary] [garak-python-binary]
# Needs Node.js for Promptfoo. Garak is skipped when no garak python is reachable.
set -uo pipefail
cd "$(dirname "$0")/.."
PY="${1:-python}"
GARAK_PY="${2:-$PY}"
RAW=reports/raw
rm -rf "$RAW" && mkdir -p "$RAW/canary"

export DEEPEVAL_TELEMETRY_OPT_OUT=YES PROMPTFOO_DISABLE_TELEMETRY=1 PROMPTFOO_DISABLE_UPDATE=1 PROMPTFOO_DISABLE_SHARING=1

scripts/start_agents.sh "$PY" || exit 1
trap 'pkill -f "agent.server" || true' EXIT

"$PY" -m pytest -q --junitxml="$RAW/unit.xml"
EVAL_RESULTS_DIR="$RAW" AGENT_URL=http://127.0.0.1:8000 "$PY" -m pytest evals/deepeval -q
EVAL_RESULTS_DIR="$RAW/canary" AGENT_URL=http://127.0.0.1:8001 "$PY" -m pytest evals/deepeval -q

PF="npx --yes promptfoo@0.125.1 eval -c evals/promptfoo/promptfooconfig.yaml --no-cache --no-progress-bar --no-table"
AGENT_URL=http://127.0.0.1:8000 $PF -o "$RAW/promptfoo.json"
AGENT_URL=http://127.0.0.1:8001 $PF -o "$RAW/canary/promptfoo.json"

evals/garak/run_garak.sh 8000 "$RAW/garak" "$GARAK_PY"
evals/garak/run_garak.sh 8001 "$RAW/canary/garak" "$GARAK_PY"

"$PY" scripts/build_report.py
echo "Report: reports/latest/index.html"
