#!/usr/bin/env bash
# Start the hardened agent on :8000 and the deliberately vulnerable one on :8001.
# Usage: scripts/start_agents.sh [python-binary]
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${1:-python}"
mkdir -p reports/raw/canary
AGENT_MODE=mock "$PY" -m agent.server --port 8000 --variant hardened   > reports/raw/agent-hardened.log 2>&1 &
AGENT_MODE=mock "$PY" -m agent.server --port 8001 --variant vulnerable > reports/raw/agent-vulnerable.log 2>&1 &
for port in 8000 8001; do
  for _ in $(seq 1 40); do
    if curl -sf "http://127.0.0.1:${port}/health" > /dev/null; then break; fi
    sleep 0.5
  done
  curl -sf "http://127.0.0.1:${port}/health" > /dev/null || { echo "agent on :${port} did not start"; exit 1; }
done
echo "agents ready: hardened :8000, vulnerable :8001"
