"""Deterministic DeepEval metrics.

They subclass BaseMetric, so they plug into assert_test and into any DeepEval
dataset run exactly like the built in metrics. They do not call a judge model,
which keeps every run free, fast and reproducible. When a real LLM judge is
available, GEval or FaithfulnessMetric can be added next to them.
"""
import re
from typing import List

from deepeval.metrics import BaseMetric
from deepeval.models import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase

STOPWORDS = {
    "the", "and", "for", "are", "with", "that", "this", "you", "your", "our", "can", "will",
    "not", "have", "has", "was", "its", "from", "all", "any", "but", "than",
}


class NoJudge(DeepEvalBaseLLM):
    """Placeholder judge for built in metrics that never need one in exact match mode."""

    def __init__(self):
        pass

    def load_model(self):
        return None

    def generate(self, prompt: str, *args, **kwargs) -> str:
        raise RuntimeError("This suite is judge free, the model must not be called")

    async def a_generate(self, prompt: str, *args, **kwargs) -> str:
        raise RuntimeError("This suite is judge free, the model must not be called")

    def get_model_name(self) -> str:
        return "no-judge"


class _SimpleMetric(BaseMetric):
    name = "Metric"

    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.score = 0.0
        self.success = False
        self.reason = ""
        self.async_mode = False
        self.strict_mode = False
        self.include_reason = True
        self.error = None
        self.evaluation_model = "deterministic"

    async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return bool(self.success)

    @property
    def __name__(self) -> str:
        return self.name


class ExpectedFactsMetric(_SimpleMetric):
    """Share of required phrases that appear in the answer."""

    name = "Expected Facts"

    def __init__(self, expected: List[str], threshold: float = 1.0):
        super().__init__(threshold)
        self.expected = expected

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        answer = test_case.actual_output.lower()
        missing = [p for p in self.expected if p.lower() not in answer]
        self.score = 1.0 if not self.expected else (len(self.expected) - len(missing)) / len(self.expected)
        self.success = self.score >= self.threshold
        self.reason = "all expected facts found" if not missing else f"missing: {missing}"
        return self.score


class ForbiddenContentMetric(_SimpleMetric):
    """Fails when the answer contains text that must never be shown."""

    name = "Forbidden Content"

    def __init__(self, forbidden: List[str], threshold: float = 1.0):
        super().__init__(threshold)
        self.forbidden = forbidden

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        answer = test_case.actual_output.lower()
        found = [p for p in self.forbidden if p.lower() in answer]
        self.score = 0.0 if found else 1.0
        self.success = self.score >= self.threshold
        self.reason = "no forbidden content" if not found else f"leaked: {found}"
        return self.score


class GroundednessMetric(_SimpleMetric):
    """Lexical groundedness: how much of the answer is supported by retrieved context or the question."""

    name = "Groundedness"

    def __init__(self, threshold: float = 0.8):
        super().__init__(threshold)

    @staticmethod
    def _terms(text: str) -> set:
        text = re.sub(r"\(source:[^)]*\)", " ", text.lower())
        return {w for w in re.findall(r"[a-z0-9.]+", text) if len(w) > 2 and w not in STOPWORDS}

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        answer_terms = self._terms(test_case.actual_output)
        support = self._terms(" ".join(test_case.retrieval_context or []) + " " + test_case.input)
        if not answer_terms:
            self.score = 1.0
        else:
            self.score = len(answer_terms & support) / len(answer_terms)
        self.success = self.score >= self.threshold
        self.reason = f"{self.score:.0%} of answer terms are supported by the retrieved context"
        return self.score

