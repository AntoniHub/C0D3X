---
description: Diagnoses a failed test run and drafts the bug report. Use when a test, a CI job or a script fails and the cause is unknown.
argument-hint: "<path to log or report, or the pasted failure>"
---
Triage this failure: $ARGUMENTS

1. Collect the failing test id, the traceback and the environment (local or CI, OS,
   Python or Node version). If the input is a path, read it.
2. Delegate to the `bug-reporter` subagent with the failure text. Do not paste
   secrets, tokens or URLs that carry a key into the delegation.
3. From its report, state the classification (product defect, test defect,
   environment, flaky) with the evidence and the confidence.
4. If the failure is a test defect or flaky, propose the smallest fix and show it
   before applying it. If it is a product defect, do not change the test to hide it.
5. Offer the report as a Markdown block ready to paste into an issue.
