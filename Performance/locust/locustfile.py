"""Locust load test for the Shopwise Support agent (OpenAI-compatible endpoint).

Deliberately tiny: one simulated user for a few seconds. It shows the structure of a
real load test (weighted tasks, response validation, pass/fail gate, HTML report)
without putting any pressure on the service.

    locust -f Performance/locust/locustfile.py --headless -u 1 -r 1 -t 6s \
        --host http://127.0.0.1:8000 --html reports/locust.html --csv reports/locust

The process exits with a non-zero code when a threshold fails.
"""
import os

from locust import HttpUser, constant, events, task

LATENCY_BUDGET_MS = float(os.getenv("LATENCY_BUDGET_MS", "2000"))
MAX_FAIL_RATIO = float(os.getenv("MAX_FAIL_RATIO", "0.01"))


class SupportAgentUser(HttpUser):
    """A customer chatting with the support agent."""

    wait_time = constant(1)  # one request per second per user, nothing aggressive

    def ask(self, name: str, prompt: str, expected_tool: str, must_include: str) -> None:
        with self.client.post(
            "/v1/chat/completions",
            json={"messages": [{"role": "user", "content": prompt}]},
            name=name,  # group stats by scenario instead of by URL
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"unexpected status {response.status_code}")
                return
            body = response.json()
            answer = body["choices"][0]["message"]["content"]
            tools = [t["name"] for t in body.get("x_agent", {}).get("tools_called", [])]
            if must_include.lower() not in answer.lower():
                response.failure(f"answer does not contain {must_include!r}")
            elif expected_tool not in tools:
                response.failure(f"{expected_tool} was not called (got {tools})")
            else:
                response.success()

    @task(3)
    def policy_question(self) -> None:
        self.ask("policy", "What is your return policy?", "search_policy", "30 days")

    @task(2)
    def order_status(self) -> None:
        self.ask(
            "order",
            "Hi, where is ORD-1001? My email is alice@example.com",
            "lookup_order",
            "shipped",
        )

    @task(1)
    def refund_calculation(self) -> None:
        self.ask("refund", "Calculate my refund for 2 items at 19.99 euros", "calculate_refund", "39.98")


@events.quitting.add_listener
def enforce_thresholds(environment, **_kwargs) -> None:
    """Turn the run into a quality gate: fail the process when a budget is broken."""
    total = environment.stats.total
    problems = []
    if total.num_requests == 0:
        problems.append("no requests were sent")
    else:
        if total.fail_ratio > MAX_FAIL_RATIO:
            problems.append(f"failure ratio {total.fail_ratio:.2%} > {MAX_FAIL_RATIO:.2%}")
        p95 = total.get_response_time_percentile(0.95)
        if p95 > LATENCY_BUDGET_MS:
            problems.append(f"p95 {p95:.0f} ms > {LATENCY_BUDGET_MS:.0f} ms")
    if problems:
        print("LOCUST GATE FAILED: " + "; ".join(problems))
        environment.process_exit_code = 1
    else:
        print(f"LOCUST GATE PASSED: {total.num_requests} requests, p95 {total.get_response_time_percentile(0.95):.0f} ms")
