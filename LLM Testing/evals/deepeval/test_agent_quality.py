"""Functional quality, safety and grounding checks written with DeepEval.

Every golden case is one pytest test. A case passes only when all of its metrics pass.
Run from the "LLM Testing" folder with the agent API already running.
"""
import json
import os
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall

from evals.common.client import AgentClient
from evals.common.recorder import record
from evals.deepeval.metrics import ExpectedFactsMetric, ForbiddenContentMetric, GroundednessMetric, NoJudge

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "YES")

CASES = json.loads((Path(__file__).parents[1] / "datasets" / "golden.json").read_text())


@pytest.fixture(scope="module")
def client():
    return AgentClient()


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_golden_case(case, client):
    messages = case.get("messages") or [{"role": "user", "content": case["input"]}]
    reply = client.chat(messages)

    test_case = LLMTestCase(
        input=messages[-1]["content"],
        actual_output=reply.content,
        retrieval_context=reply.retrieval_context or None,
        tools_called=[ToolCall(name=name) for name in reply.tools_called],
        expected_tools=[ToolCall(name=name) for name in case["expected_tools"]],
    )

    metrics = [
        ToolCorrectnessMetric(
            threshold=1.0, model=NoJudge(), should_exact_match=True, async_mode=False, include_reason=False
        )
    ]
    if case["must_include"]:
        metrics.append(ExpectedFactsMetric(case["must_include"]))
    if case["must_not_include"]:
        metrics.append(ForbiddenContentMetric(case["must_not_include"]))
    if reply.retrieval_context:
        metrics.append(GroundednessMetric(threshold=0.8))

    error = None
    try:
        assert_test(test_case, metrics, run_async=False)
    except AssertionError as exc:
        error = str(exc)
        raise
    finally:
        record(
            "deepeval",
            {
                "id": case["id"],
                "category": case["category"],
                "input": test_case.input,
                "output": reply.content,
                "tools_called": reply.tools_called,
                "expected_tools": case["expected_tools"],
                "latency_ms": reply.latency_ms,
                "passed": error is None,
                "metrics": [
                    {
                        "name": getattr(m, "__name__", type(m).__name__),
                        "score": None if m.score is None else round(float(m.score), 3),
                        "passed": bool(m.is_successful()),
                        "reason": getattr(m, "reason", "") or "",
                    }
                    for m in metrics
                ],
            },
        )
