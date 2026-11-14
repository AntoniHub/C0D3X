# Performance testing: k6 and Locust

Latency and load checks for the **Shopwise Support agent**, the OpenAI-compatible FastAPI endpoint built in [LLM Testing](../LLM%20Testing). Testing the agent's own endpoint ties performance to the LLM evaluation work: the same questions, the same latency budget (2000 ms, as in the Promptfoo assertions).

The scripts are deliberately small. One virtual user and a handful of requests are enough to show the structure of a performance test and to act as a regression gate. Nothing here puts real pressure on the service.

| Tool | File | What it shows |
|---|---|---|
| k6 | [`k6/chat-latency.js`](k6/chat-latency.js) | Scenarios, thresholds on p95 latency and error rate, checks on the response body, a custom metric for server-side latency, a summary file |
| Locust | [`locust/locustfile.py`](locust/locustfile.py) | A user class with weighted tasks, response validation with `catch_response`, grouped statistics, an HTML report and a pass/fail gate |

Both runs exit with a non-zero code when a budget is broken, so the CI job turns red.

## Run it locally

```bash
pip install -r "LLM Testing/requirements.txt" -r Performance/requirements.txt
# install k6: https://grafana.com/docs/k6/latest/set-up/install-k6/
Performance/scripts/run_local.sh python
```

Or step by step, with the agent already running on port 8000:

```bash
k6 run Performance/k6/chat-latency.js
python -m locust -f Performance/locust/locustfile.py --headless -u 1 -r 1 -t 6s \
  --host http://127.0.0.1:8000 --html Performance/reports/locust.html
```

Useful settings: `BASE_URL`, `ITERATIONS` (k6), `LATENCY_BUDGET_MS`, `MAX_FAIL_RATIO` (Locust).

## In CI

[`performance.yml`](../.github/workflows/performance.yml) runs on every change to `Performance/` or the agent, every day at 13:00 UTC and on demand. It starts the agent, runs k6 and Locust, writes a summary table to the run page and uploads the reports as artifacts.

## What I would add for a real service

- Load stages (ramp up, hold, ramp down) and a stress profile in a separate scenario, run against a dedicated environment.
- Percentile budgets per endpoint, stored as thresholds in version control.
- Token-based metrics and cost per request once the agent uses a real model.
- Results pushed to Grafana or another dashboard to compare runs over time.
