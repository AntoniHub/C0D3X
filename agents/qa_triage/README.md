# qa-triage

A small agent that turns a failed test run into a classified issue. Code does everything that is
deterministic; the model is called only for the one thing that needs judgement: deciding whether a
failure is a product defect, a test defect, an environment problem or a flaky test.

```
JUnit XML -> parse -> redact secrets -> fingerprint -> (new failure?) -> model classifies -> Markdown issue
```

## Design decisions

| Decision | Why |
|---|---|
| Parse and redact before anything else | Secrets are removed at the parser, so no later step can leak them, including the model call and the issue body |
| Fingerprint of test ids and normalised messages | A failure that is already known is recognised without a model call. The workflow compares it with the open issues |
| Structured output validated against a schema | The verdict is a typed object, never free text to parse |
| Failure text delimited and declared untrusted | Test output can contain instructions; the prompt says to ignore them, and the schema limits what a reply can be |
| `defusedxml` for the reports | Reports come from CI artifacts, so entity expansion is rejected |
| No key, no failure | Without `ANTHROPIC_API_KEY` the report is still produced, marked "not triaged", and the exit code is 0 |
| Small model by default | `claude-haiku-5-5`; change it with `QA_TRIAGE_MODEL` |

## Use

```bash
pip install -e ".[dev]"
qa-triage fingerprint reports/api-offline.xml        # prints the fingerprint, or "none"
qa-triage triage reports/*.xml --dry-run              # no model call
ANTHROPIC_API_KEY=... qa-triage triage reports/*.xml --out issue.md
```

## Test

```bash
ruff check . && ruff format --check . && mypy && pytest --cov
```

The tests use a stub client, so they need no key and no network. The call to the real API has not
been exercised yet.
