# Test Plan: api-weather-client

## 1. Identification and scope

- Identifier: TP-API-WEATHER-CLIENT
- Version: 1.0 (2026-11-21), status: draft
- Test items: `weather_client` package 0.1.0 in `API-Pytest/src/weather_client` (`WeatherClient`, `Units`, models, error hierarchy, `Settings`), plus `schemas/current_weather.schema.json` as the published contract.
- In scope: request building, input validation, response parsing and contract checks, error mapping, retry/backoff, secret handling, live behaviour of the OpenWeather `/weather` endpoint as consumed by the client.
- Out of scope: other OpenWeather endpoints, OpenWeather's own correctness (weather accuracy), load testing of the provider, UI.

Test case IDs (TC-API-NNN) live in this plan only. Existing tests do not carry them in a marker or in their names. Adopting an id marker is an open item (section 7). Until then the matrix maps ids to pytest node ids.

## 2. Risk analysis

| ID | Risk | L | I | How testing addresses it |
|----|------|---|---|--------------------------|
| R1 | API key leaks via exception text, `__cause__`, logs or reports | M | H | TC-API-023, TC-API-041; live fixtures drop original errors; section 4 rules |
| R2 | Wrong error class or lost status code, so callers mis-handle failures | M | H | TC-API-010 to 012 |
| R3 | Retry storm or unbounded wait (retrying 4xx, uncapped Retry-After) | M | H | TC-API-010, 013 to 020 |
| R4 | Provider changes payload shape, client silently returns bad data | M | H | TC-API-001 to 009, 030, 031 (live schema) |
| R5 | Invalid input reaches the API and burns quota | M | M | TC-API-004 to 008 |
| R6 | Live suite exhausts free-tier quota or flakes on provider outage | M | M | 9-request budget, skip without key, live job not run on pull requests |
| R7 | Insecure or invalid configuration accepted (http URL, bad timeout) | L | M | TC-API-042 |
| R8 | Gaps in untested behaviours (see "not automated") | M | M | Listed in the matrix and section 7 |

Priority order: R1, R2, R3, R4 first (P1), then R5, R6, R7.

## 3. Test approach

| Level | Scope | Tooling |
|-------|-------|---------|
| Unit | Client logic with stubbed HTTP and an injected `sleep` (no real waiting) | pytest, `responses` |
| Contract | Sample payload vs JSON schema; model parsing vs payload mutations; live response vs schema | `jsonschema`, pydantic strict models |
| Integration (live) | Real endpoint, raw requests plus one typed client call | pytest `-m live` |
| End to end | Same as live; the client has no other tiers | n/a |
| Performance | Not planned. Timeouts and backoff are verified by value, not by load | n/a |

Static gates in CI: `ruff check`, `ruff format --check`, `mypy` (strict), offline coverage floor 90% (branch coverage).

Design techniques and why:
- Equivalence partitioning: status codes by class (400/401/404 mapped and not retried; 429/5xx retried; other, such as 418, base error). Fewest cases that cover each error branch.
- Boundary values: lat/lon at +-90 and +-180 and just beyond; `max_retries` of 0 and -1; Retry-After above the 30 s cap. Range checks are where off-by-one errors occur.
- Decision table: retry decision from (status or exception, attempt < max_retries, Retry-After numeric or not) gives wait value or raise (TC-API-013 to 020).
- State transition: retry loop attempts 0..max, ending in success or exhaustion (TC-API-017, 018).
- Error guessing: payload mutations (null, numeric string, empty list), non-JSON bodies, error payload with 200, key inside exception text.

## 4. Environment, data and tooling

- Python 3.11+ (CI uses 3.12 on ubuntu-latest); install with `pip install -e ".[dev]"`.
- Offline: no network, no secrets. Data: `tests/data/current_weather_madrid.json`, `schemas/current_weather.schema.json`.
- Live: needs `OWM_API_KEY`. Supplied by an environment variable (CI: repository secret mapped to env) or a local untracked `.env` (template `.env.example` has an empty value). The key is never committed, never printed, and never written to reports (JUnit, HTML, step summary). `Settings` holds it as `SecretStr`. Without a key, live tests skip with a reason.
- Reports: `reports/report.html` and JUnit XML, uploaded as artifacts for 7 days. Reviewers must check the artifacts contain no key before sharing.
- Commands: offline `pytest -m "not live"`; live `pytest -m live -rs`.

## 5. Entry and exit criteria

Entry: dependencies install; ruff and mypy pass; for live runs the key is configured and the quota budget is available.

Exit (offline, every push and pull request): all offline tests pass, coverage at least 90%, lint and types clean.
Exit (live, push, nightly 15:00 UTC cron, manual): all 9 live requests succeed or skip because no key is configured.

When criteria are not met:
- Offline failure or coverage below 90%: the build fails and the change is not merged until fixed or the gap is documented here.
- Live failure: first classify as provider outage, quota or key problem, or real defect. A defect blocks release. An outage or quota issue is re-run once later (not immediately, to save quota) and recorded. Live results never gate pull requests.
- Live skipped in CI: treated as "not verified", not as a pass. Reported via `-rs`.

## 6. Traceability matrix

Paths relative to `API-Pytest/`. Status "Auto" means a test exists today; ids are not yet in markers or names.

| TC ID | Behaviour | Level | Pytest node id (file::test) | Status |
|-------|-----------|-------|-----------------------------|--------|
| TC-API-001 | Sample payload conforms to schema | Contract | tests/mocked/test_client_contract.py::test_sample_payload_conforms_to_the_published_schema | Auto |
| TC-API-002 | Valid payload parsed into typed model | Unit | tests/mocked/test_client_contract.py::test_valid_payload_is_parsed_into_the_model | Auto |
| TC-API-003 | Optional sections absent give None; precipitation volumes; int to float; unknown fields ignored | Unit | tests/mocked/test_client_contract.py::test_optional_sections_may_be_absent, ::test_precipitation_volumes_are_exposed, ::test_integer_measurements_are_accepted_as_floats, ::test_unknown_fields_are_ignored | Auto |
| TC-API-004 | Blank city rejected before any HTTP call | Unit | tests/mocked/test_client_requests.py::test_blank_city_is_rejected_without_calling_the_api | Auto |
| TC-API-005 | Out-of-range coordinates rejected before HTTP | Unit | tests/mocked/test_client_requests.py::test_out_of_range_coordinates_are_rejected_without_calling_the_api | Auto |
| TC-API-006 | Boundary coordinates accepted | Unit | tests/mocked/test_client_requests.py::test_boundary_coordinates_are_accepted | Auto |
| TC-API-007 | Empty api_key and negative max_retries rejected | Unit | tests/mocked/test_client_requests.py::test_empty_api_key_is_rejected, ::test_negative_retry_count_is_rejected | Auto |
| TC-API-008 | NaN or infinite lat/lon, non-str inputs | Unit | none | Not automated |
| TC-API-009 | Contract-violating payloads and non-object bodies raise MalformedResponseError; error payload with 200 rejected | Unit | tests/mocked/test_client_contract.py::test_payloads_violating_the_contract_are_rejected, ::test_bodies_that_are_not_json_objects_are_rejected, ::test_error_payload_served_with_a_success_status_is_rejected | Auto |
| TC-API-010 | 400/401/404 mapped to typed errors with status and message, not retried | Unit | tests/mocked/test_client_errors.py::test_client_errors_are_mapped_and_never_retried | Auto |
| TC-API-011 | Non-JSON error body gives generic message | Unit | tests/mocked/test_client_errors.py::test_non_json_error_body_falls_back_to_a_generic_message | Auto |
| TC-API-012 | Unexpected status (418) maps to base error | Unit | tests/mocked/test_client_errors.py::test_unexpected_status_maps_to_the_base_error | Auto |
| TC-API-013 | 429 retried then succeeds with base backoff | Unit | tests/mocked/test_client_resilience.py::test_rate_limited_request_is_retried_and_succeeds | Auto |
| TC-API-014 | Retry-After overrides backoff | Unit | tests/mocked/test_client_resilience.py::test_retry_after_header_overrides_the_backoff | Auto |
| TC-API-015 | Retry-After capped at 30 s | Unit | tests/mocked/test_client_resilience.py::test_retry_after_header_is_capped | Auto |
| TC-API-016 | Non-numeric Retry-After falls back to backoff | Unit | tests/mocked/test_client_resilience.py::test_non_numeric_retry_after_falls_back_to_the_backoff | Auto |
| TC-API-017 | Exponential backoff across 5xx | Unit | tests/mocked/test_client_resilience.py::test_backoff_grows_exponentially_across_server_errors | Auto |
| TC-API-018 | Retries exhausted raise UpstreamError / RateLimitError | Unit | tests/mocked/test_client_resilience.py::test_persistent_server_error_is_raised_after_exhausting_retries, ::test_persistent_rate_limit_is_raised_after_exhausting_retries | Auto |
| TC-API-019 | Retries disabled with max_retries=0 | Unit | tests/mocked/test_client_resilience.py::test_retries_can_be_disabled | Auto |
| TC-API-020 | Timeout retried and recovers | Unit | tests/mocked/test_client_resilience.py::test_timeout_is_retried_and_recovers | Auto |
| TC-API-021 | Backoff above 30 s capped without Retry-After; 501 and other non-retryable 5xx not retried | Unit | none | Not automated |
| TC-API-022 | Timeout value passed to the HTTP call | Unit | none | Not automated |
| TC-API-023 | Persistent network failure never leaks key, no `__cause__` | Unit | tests/mocked/test_client_resilience.py::test_persistent_network_failure_never_leaks_the_api_key | Auto |
| TC-API-024 | City request defaults to metric; units and lang forwarded | Unit | tests/mocked/test_client_requests.py::test_city_request_defaults_to_metric_units, ::test_city_request_forwards_units_and_language | Auto |
| TC-API-025 | City trimmed before sending | Unit | tests/mocked/test_client_requests.py::test_city_name_is_trimmed_before_sending | Auto |
| TC-API-026 | Coordinates request sends lat/lon | Unit | tests/mocked/test_client_requests.py::test_coordinates_request_sends_lat_and_lon | Auto |
| TC-API-027 | Trailing slash in base URL tolerated | Unit | tests/mocked/test_client_requests.py::test_trailing_slash_in_base_url_is_tolerated | Auto |
| TC-API-028 | Empty `lang` omitted from the query | Unit | none | Not automated |
| TC-API-029 | Key not exposed via `str`/`repr` of client or models | Unit | none | Not automated |
| TC-API-030 | Live: city query returns 200 JSON, resolves Madrid/ES, plausible temperature, recent timestamp | Live | tests/live/test_current_weather_live.py::test_city_query_returns_a_json_success_response, ::test_city_query_resolves_to_madrid_spain, ::test_metric_temperature_is_physically_plausible, ::test_observation_timestamp_is_recent | Auto |
| TC-API-031 | Live response conforms to schema | Live | tests/live/test_current_weather_live.py::test_city_query_response_conforms_to_the_schema | Auto |
| TC-API-032 | Live imperial consistent with metric | Live | tests/live/test_current_weather_live.py::test_imperial_temperature_is_consistent_with_metric | Auto |
| TC-API-033 | Live coordinates resolve same area | Live | tests/live/test_current_weather_live.py::test_coordinates_query_resolves_the_same_area_as_the_city_query | Auto |
| TC-API-034 | Live missing or invalid key gives 401 | Live | tests/live/test_current_weather_live.py::test_requests_without_a_valid_key_are_unauthorized | Auto |
| TC-API-035 | Live unknown city gives 404 | Live | tests/live/test_current_weather_live.py::test_unknown_city_returns_not_found | Auto |
| TC-API-036 | Live missing location gives 400 | Live | tests/live/test_current_weather_live.py::test_request_without_location_is_rejected | Auto |
| TC-API-037 | Live out-of-range latitude gives 400 | Live | tests/live/test_current_weather_live.py::test_out_of_range_latitude_is_rejected | Auto |
| TC-API-038 | Live typed client call returns parsed model | Live | tests/live/test_current_weather_live.py::test_client_returns_a_typed_result_from_the_real_api | Auto |
| TC-API-039 | Live tests skip cleanly without key | Live | none (behaviour in `tests/live/conftest.py::api_key`, never asserted) | Not automated |
| TC-API-040 | Schema negative cases (schema rejects bad payloads) | Contract | none | Not automated |
| TC-API-041 | Key absent from JUnit/HTML reports | Process | none (manual artifact review) | Not automated |
| TC-API-042 | `Settings` defaults are safe; rejects non-https base URL and timeouts that are zero, negative, above 60 s or not finite; normalises the base URL | Unit | tests/mocked/test_settings.py::test_defaults_are_safe, ::test_rejects_unreasonable_timeouts, ::test_rejects_non_https_base_url, ::test_base_url_is_normalised | Auto |
| TC-API-043 | Performance / load | Performance | none | Not planned |

Live request budget per run: 1 (shared Madrid metric) + 1 imperial + 1 coordinates + 2 key cases + 1 unknown city + 1 no location + 1 latitude + 1 typed client = 9 requests. Adding a live test must update this count.

## 7. Assumptions, constraints, open questions

Constraints:
- The live suite makes 9 HTTP requests per run to protect the free-tier quota. Scheduled daily plus push runs must stay within it. Do not add live tests without need; prefer offline cases.
- Live results depend on provider availability and current weather, so assertions use tolerances (3 degrees, 0.1 degrees coordinates, 24 h timestamp).

Assumptions:
- The sample payload is representative of the provider response; the schema was written from it and from documentation.
- Coverage figure is enforced in CI only for offline tests.

Open questions and items:
1. Adopt a marker (for example `@pytest.mark.tc("TC-API-001")`) or ids in test names so tests reference the plan; today none do. Needs a registered marker under `--strict-markers`.
2. Is the 90% coverage floor adequate? Offline coverage is currently 100% of the package.
3. Should the schema (which requires `cod` and has no `rain`/`snow`/`sys`/`visibility`) be aligned with the models, and get negative tests (TC-API-040)?
4. Pull requests from forks never run live tests; accept this or add a manual trigger?
5. Cause of 4xx other than 400/401/404/429 (for example 403) mapping to the base error is verified only for 418.
