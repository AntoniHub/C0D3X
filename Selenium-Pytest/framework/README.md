# Selenium + pytest reference framework

A small, readable Selenium 4 framework that shows how I structure UI automation so it stays maintainable: Page Object Model, explicit waits only, fixtures for setup, evidence on failure and a browser matrix in CI.

It runs against the bundled [demo app](../../demo-app), so it is deterministic, needs no credentials and works offline. Point `BASE_URL` at any other deployment to reuse the same suite.

```
framework/
├── config.py          settings from environment variables, no values in test code
├── conftest.py        app under test, browser factory, page-object fixtures, failure evidence
├── pages/             Page Objects: one class per page, methods describe user intent
│   ├── base_page.py   explicit waits and shared actions
│   └── login_page.py, inventory_page.py, cart_page.py, checkout_page.py
└── tests/             tests read like scenarios and never touch the driver
    ├── test_login.py, test_cart.py, test_checkout.py
```

## Design decisions

| Decision | Why |
|---|---|
| Page Objects with intent-level methods (`login()`, `add()`, `checkout()`) | A UI change is fixed in one class, not in every test |
| `data-testid` locators, no absolute XPath | Layout and CSS changes do not break tests |
| Explicit waits only (`WebDriverWait` + expected conditions), no `time.sleep` | Faster when the app is fast, stable when it is slow |
| A fresh browser per test, login through a fixture | Tests are independent and can run in any order or in parallel |
| `pytest.mark.parametrize` for validation cases | Eight scenarios, one test body |
| Selenium Manager, no driver paths | No `C:/Drivers/chromedriver.exe` on one machine; works the same in CI |
| Screenshot, page source and URL saved on failure, embedded in the HTML report | A red run can be diagnosed without re-running it |
| Markers `smoke` and `regression` | Run the 3-test smoke set on every commit and the rest nightly |

## Run it

```bash
pip install -r requirements.txt
pytest                                   # Chrome, headless, bundled demo app
pytest -m smoke                          # fast subset
pytest --selenium-browser firefox        # or edge
HEADLESS=0 pytest                        # watch the browser
BASE_URL=https://staging.example.com pytest
```

The HTML report is written to `reports/report.html`. CI runs the suite on Chrome and Firefox every day and on every change: see [`ui-tests.yml`](../../.github/workflows/ui-tests.yml).
