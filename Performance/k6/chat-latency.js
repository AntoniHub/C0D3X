// k6 smoke/latency test for the Shopwise Support agent (OpenAI-compatible endpoint).
//
// Deliberately tiny: 1 virtual user and a handful of iterations. The goal is a
// repeatable latency and correctness gate, not to stress the service.
//
//   k6 run Performance/k6/chat-latency.js
//   k6 run -e BASE_URL=http://127.0.0.1:8000 -e ITERATIONS=5 Performance/k6/chat-latency.js
//
// The run exits with a non-zero code when a threshold fails, so CI turns red.
import http from "k6/http";
import { check, sleep } from "k6";
import { Trend } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:8000";
const ITERATIONS = parseInt(__ENV.ITERATIONS || "3", 10);
// Same budget as the Promptfoo latency assertion in LLM Testing.
const LATENCY_BUDGET_MS = parseInt(__ENV.LATENCY_BUDGET_MS || "2000", 10);

// Server-side time reported by the agent (x_agent.latency_ms), tracked apart
// from the HTTP round trip so a slow network is not mistaken for a slow agent.
const agentLatency = new Trend("agent_latency_ms", true);

export const options = {
  scenarios: {
    smoke: {
      executor: "shared-iterations",
      vus: 1,
      iterations: ITERATIONS,
      maxDuration: "1m",
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: [`p(95)<${LATENCY_BUDGET_MS}`],
    agent_latency_ms: [`p(95)<${LATENCY_BUDGET_MS}`],
    checks: ["rate==1"],
  },
};

// Same questions as the golden dataset, so performance and quality share one language.
const REQUESTS = [
  { name: "policy", prompt: "What is your return policy?", expectedTool: "search_policy", mustInclude: "30 days" },
  {
    name: "order",
    prompt: "Hi, where is ORD-1001? My email is alice@example.com",
    expectedTool: "lookup_order",
    mustInclude: "shipped",
  },
  {
    name: "refund",
    prompt: "Calculate my refund for 2 items at 19.99 euros",
    expectedTool: "calculate_refund",
    mustInclude: "39.98",
  },
];

export function setup() {
  const health = http.get(`${BASE_URL}/health`);
  if (health.status !== 200) {
    throw new Error(`Agent is not reachable at ${BASE_URL} (status ${health.status})`);
  }
}

export default function () {
  const scenario = REQUESTS[__ITER % REQUESTS.length];
  const res = http.post(
    `${BASE_URL}/v1/chat/completions`,
    JSON.stringify({ messages: [{ role: "user", content: scenario.prompt }] }),
    { headers: { "Content-Type": "application/json" }, tags: { scenario: scenario.name } },
  );

  const body = res.status === 200 ? res.json() : {};
  const answer = body.choices && body.choices[0] ? body.choices[0].message.content : "";
  const agent = body.x_agent || {};

  if (typeof agent.latency_ms === "number") {
    agentLatency.add(agent.latency_ms, { scenario: scenario.name });
  }

  check(res, {
    "status is 200": (r) => r.status === 200,
    [`${scenario.name}: answer contains "${scenario.mustInclude}"`]: () =>
      answer.toLowerCase().includes(scenario.mustInclude.toLowerCase()),
    [`${scenario.name}: ${scenario.expectedTool} was called`]: () =>
      (agent.tools_called || []).some((t) => t.name === scenario.expectedTool),
  });

  sleep(0.5);
}

export function handleSummary(data) {
  const m = data.metrics;
  const ms = (metric, stat) => (m[metric] && m[metric].values[stat] !== undefined ? m[metric].values[stat].toFixed(1) : "n/a");
  const lines = [
    "",
    "k6 summary | Shopwise Support agent",
    `  requests        ${m.http_reqs.values.count}`,
    `  failed          ${(m.http_req_failed.values.rate * 100).toFixed(2)} %`,
    `  http p95        ${ms("http_req_duration", "p(95)")} ms (budget ${LATENCY_BUDGET_MS} ms)`,
    `  agent p95       ${ms("agent_latency_ms", "p(95)")} ms (server side)`,
    `  checks passed   ${(m.checks.values.rate * 100).toFixed(0)} %`,
    "",
  ];
  return {
    stdout: lines.join("\n"),
    "reports/k6-summary.json": JSON.stringify(data, null, 2),
  };
}

