# Playwright + pytest reference framework

A compact Playwright (Python) framework that shows how I design UI and API automation: Page Objects, web-first assertions, authentication reused as storage state, isolated contexts, network interception and full evidence for failures.

It runs against the bundled [demo app](../../demo-app), so it is deterministic and needs no credentials. Set `BASE_URL` to point it at another deployment.

```
framework/
├── config.py        settings from environment variables
├── conftest.py      app under test, shared login state, isolated contexts, API client
├── pages/           Page Objects built on get_by_test_id locators
└── tests/
    ├── test_login.py          validation scenarios (parametrized), anonymous access
    ├── test_shopping.py       cart, sorting, logout, end-to-end purchase, checkout validation
    └── test_api_and_ui.py     API contract, UI/API consistency, simulated backend failure
```

## Design decisions

| Decision | Why |
|---|---|
| Web-first assertions (`expect(locator)...`) | They retry until the condition holds, so there are no sleeps and no hand-written waits |
| Login once, reuse `storage_state` | Tests that are not about login start authenticated: faster and less flaky |
| One isolated browser context per test | No shared cookies or cart, tests run in any order or in parallel |
| `get_by_test_id` locators in Page Objects | Locators survive layout and style changes; tests read as user intent |
| Playwright's `APIRequestContext` for API checks | UI and API tests share one tool, one config and one report |
| `page.route` to fake a 500 | Failure paths are tested without breaking a real backend |
| Trace and screenshot kept only on failure (video too for tests without login state) | Small artifacts, full evidence: open the trace to replay the failure step by step |
| Markers `smoke`, `regression`, `api` | Fast subset on every commit, everything nightly |

## Run it

```bash
pip install -r requirements.txt
playwright install --with-deps chromium firefox
pytest                                  # Chromium
pytest --browser firefox                # or webkit, or several: --browser chromium --browser firefox
pytest -m smoke                         # fast subset
pytest --headed --slowmo 300            # watch it
playwright show-trace reports/artifacts/<failed-test>/*.zip
```

CI runs the suite on Chromium and Firefox every day and on every change: see [`ui-tests.yml`](../../.github/workflows/ui-tests.yml).

