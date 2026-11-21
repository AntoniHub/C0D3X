# C0D3X

Public QA automation portfolio of Antonio Rodriguez Farias. The global rules in
`~/.claude/CLAUDE.md` apply; this file adds the project context.

## Layout and commands

| Folder | Content | Check it with |
|---|---|---|
| `API-Pytest` | Typed weather API client, offline and live pytest suites | `ruff check . && ruff format --check . && mypy && pytest -m "not live" --cov` |
| `Selenium-Pytest/framework` | Selenium 4 and pytest against `demo-app` | `pip install -r requirements.txt && pytest` |
| `Playwright-Pytest/framework` | Playwright and pytest against `demo-app` | `playwright install chromium && pytest` |
| `LLM Testing` | LangGraph agent and its evaluation harness | see its README |
| `Performance` | k6 and Locust against the agent endpoint | see its README |
| `demo-app` | Flask store used as a local target | `python demo-app/app.py --port 5000` |
| `agents/qa_triage` | Failure triage agent (Anthropic API) | `pytest` inside the folder |
| `.claude`, `ai-config` | Subagents, skills, hooks and installer for the AI workflow | `pytest .claude/hooks` |
| `legacy` | Earlier suites kept as a record; do not modify | none |

Run every command from the folder of the suite.

## Conventions

- UI tests: Page Objects with intent-level methods, `data-testid` locators, explicit
  waits or web-first assertions, no sleeps, tests never touch the driver.
- API tests exercise `WeatherClient`, not stubs. Offline tests need no network or
  secrets. Live tests carry the `live` marker and skip when `OWM_API_KEY` is unset.
- Test case IDs follow `TC-<AREA>-<NNN>` and appear in markers or test names. Test
  plans live in `docs/test-plans/`.
- Secrets come from environment variables or an untracked `.env`. Never print or
  log a URL that carries a key.
- Commit subject is exactly `QA Engineer | Antonio Rodriguez Farias`; the body
  describes the change. Commit only when the user asks.
- Scheduled workflows push reports to `master`, so the remote moves daily. Fetch
  before branching and prefer new branches over editing `master`.
- `LLM Testing/reports` and the latest-run block of its README are generated; do not
  edit them by hand.

## Review gate

After a change, run `code-reviewer` and `security-reviewer` on the changed files.
Use `bug-reporter` for any failed run and `test-planner` before a new module.
