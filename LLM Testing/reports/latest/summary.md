### LLM Testing: PASS

Run: 2026-11-14 17:40 UTC | trigger: schedule | commit: `e8116d4`

| Suite (hardened agent) | Passed | Rate | Result |
|---|---|---|---|
| Unit tests | 20/20 | 100% | PASS |
| DeepEval | 21/21 | 100% | PASS |
| Promptfoo | 14/14 | 100% | PASS |
| Garak | 7/7 | 100% | PASS |

| Detection check (vulnerable agent) | Checks | Failed | Verdict |
|---|---|---|---|
| deepeval | 21 | 5 | CAUGHT |
| promptfoo | 14 | 6 | CAUGHT |
| garak | 7 | 5 | CAUGHT |

_QA Engineer | Antonio Rodriguez Farias_
