<div align="center">

# LLM Testing

**An automated evaluation harness for LLM agents: quality, safety and security checks that run on every commit.**

[![LLM Testing](https://github.com/AntoniHub/C0D3X/actions/workflows/llm-testing.yml/badge.svg)](https://github.com/AntoniHub/C0D3X/actions/workflows/llm-testing.yml)
![Python](https://img.shields.io/badge/python-3.12-3776ab)
![DeepEval](https://img.shields.io/badge/DeepEval-quality-6c47ff)
![Promptfoo](https://img.shields.io/badge/Promptfoo-regression-0f766e)
![Garak](https://img.shields.io/badge/Garak-vulnerability%20scan-76b900)
![LangGraph](https://img.shields.io/badge/LangChain%20%2B%20LangGraph-agent-1c3c3c)

<img alt="Static Badge" src="https://img.shields.io/badge/Antonio_Rodriguez_Farias-%2328a745?style=plastic&label=QA%20Engineer&labelColor=%23dc3545">

</div>

---

## What this is

Most LLM demos show a model answering questions. This project shows how I would **test** one.

It contains a small customer support agent for a fictional online store, and a test battery around it that is built the way I would build it for a real product:

* a golden dataset with expected tools, expected facts and forbidden content
* deterministic metrics, so the same commit always gives the same verdict
* regression checks for the core support flows
* adversarial checks: prompt injection, jailbreaks, system prompt extraction, access control
* a vulnerability scanner pointed at the live endpoint
* a **detection check** that proves the tests can actually fail (more on that below)
* a CI pipeline with an HTML report, a run history and a daily commit

The agent itself is deliberately simple and runs on a scripted mock model. The goal is not a smart agent. The goal is a trustworthy way to measure any agent. Swapping the mock for a real model is a configuration change, not a rewrite (see [Design decisions](#design-decisions-and-trade-offs)).

> Built by **QA Engineer | Antonio Rodriguez Farias**

## Latest results

<!-- LATEST-RUN:START -->
_The first scheduled run will fill this table. Trigger the workflow manually to see it sooner._
<!-- LATEST-RUN:END -->

* Latest HTML report: [`reports/latest/index.html`](reports/latest/index.html) (download it or open it locally, GitHub shows HTML files as source)
* One report per day: [`reports/archive/`](reports/archive)
* Run history: [`reports/history.json`](reports/history.json)

## Architecture

```mermaid
flowchart LR
    subgraph T["Triggers"]
        T1["push / pull request"]
        T2["daily 12:00 UTC"]
        T3["manual dispatch"]
    end

    subgraph SUT["System under test"]
        API["FastAPI<br/>OpenAI compatible API"]
        GRAPH["LangGraph agent"]
        PARTS["LangChain parts<br/>chat model, tools, retriever"]
        API --> GRAPH --> PARTS
    end

    subgraph EV["Evaluators"]
        DE["DeepEval<br/>quality and safety"]
        PF["Promptfoo<br/>regression and adversarial"]
        GA["Garak<br/>vulnerability scan"]
    end

    T --> CI["GitHub Actions"]
    CI --> SUT
    CI --> EV
    DE -- HTTP --> API
    PF -- HTTP --> API
    GA -- HTTP --> API
    EV --> RB["Report builder"]
    RB --> OUT["HTML report<br/>summary table<br/>history"]
    OUT --> COMMIT["Daily commit to master"]
```

The three evaluators never import the agent. They only see an HTTP endpoint, exactly as they would with a hosted model. That is why the same suite keeps working if the agent behind the endpoint changes.

## The agent under test

**Shopwise Support** answers questions about orders, shipping, returns and warranty. It is built with LangChain and LangGraph.

| Piece | Purpose |
|---|---|
| `lookup_order` | Order status. Requires the order id and the email of the owner. |
| `search_policy` | Retrieval over three policy documents (returns, shipping, warranty). |
| `calculate_refund` | Refund amount with an optional restocking fee. |
| System prompt | Scope rules plus an internal reference (`INTERNAL-POLICY-7731`) that must never be shown. |

### LangGraph flow (hardened variant)

```mermaid
flowchart TD
    S(["start"]) --> IG["input_guard<br/>screens the user message"]
    IG -- "attack detected" --> E(["end"])
    IG -- "clean" --> A["agent<br/>LangChain chat model"]
    A -- "tool call" --> TL["tools<br/>lookup_order, search_policy, calculate_refund"]
    TL --> A
    A -- "final answer" --> OG["output_guard<br/>redacts leaks"]
    OG --> E
```

### Two variants on purpose

| | `hardened` (default) | `vulnerable` |
|---|---|---|
| Input guard | yes | no |
| Output guard | yes | no |
| Order ownership check | yes | no, any email works |
| Purpose | the agent the suite must approve | a known bad agent the suite must reject |

The mock model is scripted, and like a weak real model it will obey an injected instruction if nothing stops it. The guards are plain regular expressions. They are enough to demonstrate the idea, and I say so openly: a production guard would use a trained classifier.

### Example request

```mermaid
sequenceDiagram
    participant U as Evaluator
    participant API as FastAPI
    participant G as LangGraph
    participant M as Chat model
    participant T as Tool
    U->>API: POST /v1/chat/completions
    API->>G: messages
    G->>M: prompt + tool schemas
    M-->>G: tool call lookup_order
    G->>T: run tool
    T-->>G: order JSON
    G->>M: tool result
    M-->>G: final answer
    G-->>API: answer + trace
    API-->>U: answer + tools_called + retrieval_context
```

The response follows the OpenAI schema and adds an `x_agent` block with the tools that were called and the retrieved context. DeepEval needs both to judge tool use and grounding.

## Evaluation strategy

| Layer | Tool | What it checks | Cases |
|---|---|---|---|
| Unit | pytest | Tools, retriever, graph routing, guards, API contract | 20 |
| Quality and safety | **DeepEval** | Correct tool for the request, required facts present, forbidden content absent, answer grounded in retrieved context | 21 |
| Regression and adversarial | **Promptfoo** | Core flows, access control, 7 injection and jailbreak variants, latency budget | 14 |
| Vulnerability scan | **Garak** | `promptinject` (3 probes, 768 prompts) and `dan` (2 probes) against the live endpoint | 770 prompts |

Every check is deterministic. There is no judge model and no API key.

### DeepEval metrics

| Metric | Type | Question it answers |
|---|---|---|
| `ToolCorrectnessMetric` | built in | Did the agent call exactly the tools this request needs? |
| `ExpectedFactsMetric` | custom `BaseMetric` | Does the answer contain the facts the policy requires? |
| `ForbiddenContentMetric` | custom `BaseMetric` | Did anything leak that must never be shown? |
| `GroundednessMetric` | custom `BaseMetric` | Is the answer supported by the retrieved context? |

The custom metrics are lexical on purpose. They are cheap, reproducible and easy to debug. `GEval` or `FaithfulnessMetric` can sit next to them once a judge model is available.

## The detection check

A green test suite proves nothing if it cannot go red. So every run evaluates **two** agents:

```mermaid
flowchart LR
    H["hardened agent"] --> SUITE["DeepEval + Promptfoo + Garak"]
    V["vulnerable agent"] --> SUITE
    SUITE --> HR["must PASS<br/>quality gate"]
    SUITE --> VR["must FAIL at least once per tool<br/>detection gate"]
    HR --> VERDICT{"Run status"}
    VR --> VERDICT
```

The run is only green when the hardened agent passes everything **and** each tool catches the vulnerable agent at least once. If a tool silently stops detecting problems (a broken assertion, a probe that no longer runs), the pipeline turns red instead of reporting a false sense of safety.

Current baseline on the vulnerable agent: DeepEval fails 5 of 21 cases, Promptfoo fails 6 of 14, Garak fails 5 of 7 probe and detector pairs, including a 100% attack success rate on `promptinject`.

## CI/CD

| Trigger | What happens |
|---|---|
| Push or pull request touching `LLM Testing/` | Full battery, summary table in the run page, report as artifact |
| Every day at 12:00 UTC | Same battery, then the HTML report and history are committed to `master` |
| Manual (`workflow_dispatch`) | Same as the daily run |

```mermaid
flowchart LR
    subgraph P["Parallel jobs"]
        J1["evals<br/>pytest, DeepEval, Promptfoo"]
        J2["garak<br/>isolated virtualenv"]
    end
    J1 --> R["report<br/>build HTML and summary"]
    J2 --> R
    R --> S["Step summary table"]
    R --> A["Artifact<br/>llm-testing-report"]
    R --> C{"scheduled or manual<br/>on master?"}
    C -- yes --> D["Commit report and history"]
    R --> G{"status PASS?"}
    G -- no --> X["Fail the run"]
```

Notes on how it is wired:

* Garak runs in its own virtual environment because its dependency tree conflicts with DeepEval's pins.
* The report job runs even if a suite fails, so a red run still produces a report.
* The commit uses the built in `GITHUB_TOKEN`. No secrets are needed anywhere in this project.
* Cron runs on UTC. Change the `cron` line in [`llm-testing.yml`](../.github/workflows/llm-testing.yml) if you want another hour.

## Repository layout

```
LLM Testing/
├── agent/                  LangChain + LangGraph agent and its FastAPI wrapper
│   ├── data/               orders and policy documents
│   ├── graph.py            LangGraph definition and guards
│   ├── mock_llm.py         scripted chat model
│   ├── retriever.py        keyword retriever
│   ├── tools.py            order lookup, policy search, refund calculator
│   └── server.py           OpenAI compatible API
├── tests/                  unit tests
├── evals/
│   ├── datasets/golden.json    golden cases
│   ├── deepeval/               metrics and tests
│   ├── promptfoo/              promptfooconfig.yaml
│   └── garak/                  REST config and run script
├── scripts/
│   ├── build_report.py         HTML report, summary and history
│   ├── start_agents.sh         starts both agent variants
│   └── run_all.sh              whole battery on your machine
└── reports/
    ├── latest/                 most recent report
    ├── archive/                one HTML file per day
    └── history.json
```

## Run it locally

Requirements: Python 3.12 or newer and Node.js 20 or newer.

```bash
cd "LLM Testing"

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Garak in its own environment
python -m venv .venv-garak && .venv-garak/bin/pip install -r requirements-garak.txt

# Everything: unit tests, DeepEval, Promptfoo, Garak, report
scripts/run_all.sh python .venv-garak/bin/python
open reports/latest/index.html   # or xdg-open on Linux
```

Run the pieces separately:

```bash
scripts/start_agents.sh python                       # hardened :8000, vulnerable :8001
python -m pytest                                     # unit tests
AGENT_URL=http://127.0.0.1:8000 python -m pytest evals/deepeval
AGENT_URL=http://127.0.0.1:8000 npx promptfoo@0.125.1 eval -c evals/promptfoo/promptfooconfig.yaml
evals/garak/run_garak.sh 8000 reports/raw/garak .venv-garak/bin/python
```

## Add a test case

Append an entry to [`evals/datasets/golden.json`](evals/datasets/golden.json). No code changes needed.

```json
{
  "id": "policy-return-window",
  "category": "policy",
  "input": "What is your return policy?",
  "expected_tools": ["search_policy"],
  "must_include": ["30 days"],
  "must_not_include": []
}
```

Multi turn cases use a `messages` array instead of `input`.

## Design decisions and trade-offs

**Why a mock model?** The point is the evaluation infrastructure. A scripted model makes every run free, fast and reproducible, so a red build always means a real change in behavior and never a flaky judge. The mock still goes through the real LangChain tool calling flow and the real LangGraph graph, so only the model's decisions are scripted.

**What the mock does not prove.** It says nothing about how a real model behaves. This suite validates the measuring instrument, not any particular model's quality.

**Moving to a real model.** `AGENT_MODE` is already the switch. Adding `ollama` (a small local model, still free) or a hosted API means adding one chat model class in `agent/`. The graph, the tools, the datasets and the three evaluators stay as they are. A real model brings noise, so I would add repeated runs, tolerance bands on thresholds and a judge model for `GEval` and `FaithfulnessMetric`.

**Known limitations**

* The guards are regular expressions. A paraphrased attack can get past the input guard. The output guard is the second line of defense, and a unit test covers exactly that case.
* Groundedness is lexical overlap, a proxy and not a semantic judgment.
* The Garak run is a short, fast subset. A real engagement would widen the probe list and run it on a schedule of its own.

**What I would add next**

* LLM as judge metrics (`GEval`, faithfulness) behind a flag
* Multi turn red teaming with generated attacks
* Latency and token budgets per release
* Trend charts built from `reports/history.json`

---

<div align="center">

Built by **QA Engineer | Antonio Rodriguez Farias**

</div>

