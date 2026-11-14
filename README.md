<img alt="Static Badge" src="https://img.shields.io/badge/Antonio_Rodriguez_Farias-%2328a745?style=plastic&label=QA%20Engineer&labelColor=%23dc3545">

# QA automation portfolio

Test automation for AI systems and for traditional software, by **Antonio Rodriguez Farias**, QA Automation Engineer. More context and write-ups: [rodriguezfarias.com](https://rodriguezfarias.com/).

| Area | Folder | What it shows |
|---|---|---|
| **LLM evaluation and AI agent testing** | [LLM Testing](LLM%20Testing) | A LangChain/LangGraph agent evaluated with DeepEval, Promptfoo and Garak: golden dataset, custom metrics, prompt injection and jailbreak tests, a detection gate and a daily GitHub Actions run. [Write-up](https://rodriguezfarias.com/llm-evaluation/) |
| **Performance** | [Performance](Performance) | k6 and Locust checks against the agent's own endpoint, with latency thresholds, a pass/fail gate and a daily CI run |
| **Frontend: Playwright** | [Playwright-Pytest/framework](Playwright-Pytest/framework) | Page Objects, web-first assertions, shared login state, API checks, network interception, trace on failure |
| **Frontend: Selenium** | [Selenium-Pytest/framework](Selenium-Pytest/framework) | Selenium 4 with Page Objects, explicit waits, fixtures, evidence on failure, Chrome and Firefox in CI |
| **Frontend: BDD** | [Cucumber-Gherkin](Cucumber-Gherkin) | Behave and Gherkin scenarios |
| **Backend, data and CI** | [Jenkins-CI](Jenkins-CI) | API test circuits with `unittest` and `requests` plus Firestore verification, Jenkins scheduling, Pentaho ETL jobs, R and Power BI |
| **Demo target** | [demo-app](demo-app) | A small Flask store used as a stable local target for the Selenium and Playwright frameworks |

The older suites in `Selenium-Pytest` (browser folders), `Cucumber-Gherkin`, `Jenkins-CI` and `Playwright-Pytest/test_playWright.py` come from earlier work against private test environments. They are kept as a record of that work, and the two `framework` folders are the cleaner reference for how I structure UI automation today.

## Continuous integration

| Workflow | Runs |
|---|---|
| [`llm-testing.yml`](.github/workflows/llm-testing.yml) | Unit tests, DeepEval, Promptfoo and Garak against a hardened and a vulnerable agent. Every change, daily 12:00 UTC |
| [`performance.yml`](.github/workflows/performance.yml) | k6 and Locust against the agent endpoint. Every change, daily 13:00 UTC |
| [`ui-tests.yml`](.github/workflows/ui-tests.yml) | Selenium (Chrome, Firefox) and Playwright (Chromium, Firefox) against the demo app. Every change, daily 14:00 UTC |

## Configuration and secrets

No credentials live in the code. The older suites read `QA_EMAIL`, `QA_API_PASSWORD`, `QA_UI_PASSWORD`, `API_KEY` and `GOOGLE_APPLICATION_CREDENTIALS` from the environment or from an untracked `.env` file. Copy [`.env.example`](.env.example) to `.env` to run them locally. The new frameworks and the LLM project need no secrets.

## Backend tests (Jenkins-CI)

* An automated endpoint test circuit makes the different API calls with the [requests](https://docs.python-requests.org/en/latest/index.html) library.
* It connects with [Cloud Firestore](https://firebase.google.com/docs/firestore/quickstart?hl=es-419#python) to read identifiers that the API responses do not return, and to verify or delete the data it created.
* Jenkins schedules the runs (freestyle project with a cron trigger).
