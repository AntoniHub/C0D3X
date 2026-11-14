#!/usr/bin/env bash
# Start the hardened support agent, run the k6 and Locust checks, then stop the agent.
# Usage: Performance/scripts/run_local.sh [python-binary]
# Requires: the "LLM Testing" requirements, Performance/requirements.txt and k6 on the PATH.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY="${1:-python}"
PORT="${AGENT_PORT:-8000}"
export BASE_URL="http://127.0.0.1:${PORT}"

mkdir -p "${ROOT}/Performance/reports"
cd "${ROOT}/LLM Testing"
AGENT_MODE=mock "$PY" -m agent.server --port "${PORT}" --variant hardened > "${ROOT}/Performance/reports/agent.log" 2>&1 &
AGENT_PID=$!
trap 'kill ${AGENT_PID} 2>/dev/null || true' EXIT

for _ in $(seq 1 40); do
  curl -sf "${BASE_URL}/health" > /dev/null && break
  sleep 0.5
done
curl -sf "${BASE_URL}/health" > /dev/null || { echo "agent did not start"; exit 1; }

cd "${ROOT}/Performance"
status=0
k6 run k6/chat-latency.js || status=1
"$PY" -m locust -f locust/locustfile.py --headless -u 1 -r 1 -t 6s \
  --host "${BASE_URL}" --html reports/locust.html --csv reports/locust || status=1
exit ${status}
