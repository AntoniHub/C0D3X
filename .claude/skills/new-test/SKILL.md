---
description: Creates a new automated test that follows this repository's conventions. Use when the user asks for a test for a behaviour, page or endpoint.
argument-hint: "<area> <behaviour to cover>"
disable-model-invocation: true
---
Create a test for: $ARGUMENTS

1. Read `CLAUDE.md` and the README of the target suite (`API-Pytest`,
   `Selenium-Pytest/framework` or `Playwright-Pytest/framework`).
2. If `docs/test-plans/` has a plan for the area, reuse its test case ID. Otherwise
   propose the next free `TC-<AREA>-<NNN>` and state it.
3. Follow the suite's pattern:
   - UI: add or extend a Page Object with intent-level methods and `data-testid`
     locators; the test reads as a scenario and never touches the driver.
   - API: write an offline test against `WeatherClient` with stubbed HTTP; add a live
     test only when the behaviour cannot be verified offline.
4. Use parametrisation for validation cases, explicit waits or web-first assertions,
   and no fixed sleeps. Carry the case ID in a marker or the test name.
5. Run the suite's checks from the folder of the suite and report the real result.
6. Delegate the changed files to `code-reviewer` and `security-reviewer`, then fix
   what they report.
