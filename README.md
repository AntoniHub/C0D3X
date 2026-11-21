<img alt="Static Badge" src="https://img.shields.io/badge/Antonio_Rodriguez_Farias-%2328a745?style=plastic&label=QA%20Engineer&labelColor=%23dc3545">

# QA automation portfolio

Test automation for AI systems and for traditional software, by **Antonio Rodriguez Farias**, QA Automation Engineer. More context and write-ups: [rodriguezfarias.com](https://rodriguezfarias.com/).

## About me

QA Automation Engineer focused on **LLM evaluation and AI agent testing**, and on automated testing of APIs, web applications and data pipelines. MSc in Big Data, Postgraduate Diploma in Defensive Cybersecurity and Diploma in Machine Learning.

I build checks that show whether a product still does what it should and stays safe while doing it: deterministic, reproducible and run on every commit, because tests only protect a product when they run. On the website I write about [LLM evaluation](https://rodriguezfarias.com/llm-evaluation/), [backend](https://rodriguezfarias.com/backend-tests/), [frontend](https://rodriguezfarias.com/frontend-tests/) and [performance](https://rodriguezfarias.com/performance-testing/) testing, and [CI/CD](https://rodriguezfarias.com/continuous-integration/).

## What is in this repository

| Area | Folder | What it shows |
|---|---|---|
| **LLM evaluation and AI agent testing** | [LLM Testing](LLM%20Testing) | A LangChain/LangGraph agent evaluated with DeepEval, Promptfoo and Garak: golden dataset, custom metrics, prompt injection and jailbreak tests, a detection gate and a daily GitHub Actions run. [Write-up](https://rodriguezfarias.com/llm-evaluation/) |
| **API testing** | [API-Pytest](API-Pytest) | A typed client for a public weather API, tested offline with stubbed HTTP (68 tests, 100% coverage, strict typing and lint) and live against the real endpoint under a request budget. Backed by a risk-based [test plan](docs/test-plans/api-weather-client.md) |
| **AI-assisted QA workflow** | [.claude](.claude), [agents](agents), [ai-config](ai-config) | The subagents, skills, hooks and triage agent I use to build and review the tests in this repository. See [How I work with AI](#how-i-work-with-ai) |
| **Performance** | [Performance](Performance) | k6 and Locust checks against the agent's own endpoint, with latency thresholds, a pass/fail gate and a daily CI run |
| **Frontend: Playwright** | [Playwright-Pytest/framework](Playwright-Pytest/framework) | Page Objects, web-first assertions, shared login state, API checks, network interception, trace on failure |
| **Frontend: Selenium** | [Selenium-Pytest/framework](Selenium-Pytest/framework) | Selenium 4 with Page Objects, explicit waits, fixtures, evidence on failure, Chrome and Firefox in CI |
| **Demo target** | [demo-app](demo-app) | A small Flask store used as a stable local target for the Selenium and Playwright frameworks |

Earlier work is kept in [legacy](legacy) as a record of how my practice evolved: `Jenkins-CI` (API test circuits with `unittest` and `requests` plus Firestore verification, Jenkins scheduling, Pentaho ETL jobs, R and Power BI), `Cucumber-Gherkin` (Behave scenarios), the browser-per-folder Selenium suites and the first Playwright script. It comes from work against private test environments. The `framework` folders and `API-Pytest` are the cleaner reference for how I structure automation today.

## How I work with AI

I use Claude Code as part of the daily QA work, and the setup is versioned here so it can be inspected and reused. Each piece has one job:

| Piece | Where | What it does |
|---|---|---|
| Project rules | [`CLAUDE.md`](CLAUDE.md) | Layout, commands and conventions the assistant reads at the start of every session |
| Subagents | [`.claude/agents`](.claude/agents) | `code-reviewer`, `security-reviewer`, `bug-reporter` (read only) and `test-planner` (writes test plans only). `code-reviewer` and `bug-reporter` run on a small model to keep token use low; the other two on a mid-size one |
| Skills | [`.claude/skills`](.claude/skills) | `/new-test`, `/triage-failure` and `/gherkin-from-story`: repeatable recipes that follow the repository conventions |
| Hooks | [`.claude/hooks`](.claude/hooks) | A guard that blocks secrets and `.env` writes, and a formatter for Python. Both have their own tests |
| MCP servers | [`.mcp.json`](.mcp.json) | Playwright, to explore a page and find stable locators, and GitHub (needs a token) |
| Triage agent | [`agents/qa_triage`](agents/qa_triage) | Reads JUnit reports, removes secrets, fingerprints the failure and uses the model only to classify it. A failure that is already known never reaches the model |
| Global setup | [`ai-config`](ai-config) | Rules and agents I install on every machine |

**What the AI does and what I decide.** The assistant drafts tests, test plans and reviews. I decide the scope, approve the plan before code is written, read every security finding, check the evidence of each run and make the commits myself. The rules forbid the assistant from committing or pushing unless I ask.

Two examples of that loop in this repository: the reviewers flagged that a network error in the live test fixture could print the API key, which I fixed and verified by hand with a dummy key, and they recommended pinning GitHub Actions to commit SHAs, which the workflows now do. The [test plan](docs/test-plans/api-weather-client.md) lists which behaviours are still not automated instead of claiming coverage.

**Current status.** The two AI workflows, [`ai-triage.yml`](.github/workflows/ai-triage.yml) and [`claude.yml`](.github/workflows/claude.yml), are complete and the triage agent is tested against a stub client. They are not connected to the API yet: they need an `ANTHROPIC_API_KEY` repository secret, and until it is set they skip with a notice and finish green. I have not run them against the live API.

## Continuous integration

| Workflow | Runs |
|---|---|
| [`llm-testing.yml`](.github/workflows/llm-testing.yml) | Unit tests, DeepEval, Promptfoo and Garak against a hardened and a vulnerable agent. Every change, daily 12:00 UTC |
| [`performance.yml`](.github/workflows/performance.yml) | k6 and Locust against the agent endpoint. Every change, daily 13:00 UTC |
| [`ui-tests.yml`](.github/workflows/ui-tests.yml) | Selenium (Chrome, Firefox) and Playwright (Chromium, Firefox) against the demo app. Every change, daily 14:00 UTC |
| [`api-tests.yml`](.github/workflows/api-tests.yml) | Lint, types and offline tests on every change, then the live tests on pushes and daily at 15:00 UTC. Actions are pinned to commit SHAs |
| [`agents-ci.yml`](.github/workflows/agents-ci.yml) | Tests for the triage agent and the Claude Code hooks |
| [`ai-triage.yml`](.github/workflows/ai-triage.yml) | After a failed API run on the default branch: opens one deduplicated issue with the classified failures. Needs `ANTHROPIC_API_KEY` |
| [`claude.yml`](.github/workflows/claude.yml) | Answers `@claude` comments from the repository owner, read only. Needs `ANTHROPIC_API_KEY` |

## Configuration and secrets

No credentials live in the code. Secrets come from the environment, an untracked `.env` file or repository secrets.

| Secret or variable | Used by | Required |
|---|---|---|
| `OWM_API_KEY` | Live tests of `API-Pytest` | No, live tests skip without it |
| `ANTHROPIC_API_KEY` | `ai-triage.yml` and `claude.yml` | No, both skip with a notice |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | The GitHub server in `.mcp.json` | Only to use that server locally |

The older suites read `QA_EMAIL`, `QA_API_PASSWORD`, `QA_UI_PASSWORD`, `API_KEY` and `GOOGLE_APPLICATION_CREDENTIALS`. Copy [`legacy/.env.example`](legacy/.env.example) to `.env` to run them locally. The frameworks and the LLM project need no secrets.

## Backend tests (legacy/Jenkins-CI)

* An automated endpoint test circuit makes the different API calls with the [requests](https://docs.python-requests.org/en/latest/index.html) library.
* It connects with [Cloud Firestore](https://firebase.google.com/docs/firestore/quickstart?hl=es-419#python) to read identifiers that the API responses do not return, and to verify or delete the data it created.
* Jenkins schedules the runs (freestyle project with a cron trigger).
