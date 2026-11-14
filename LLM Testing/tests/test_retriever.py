import pytest

from agent.retriever import build_retriever


@pytest.mark.parametrize(
    "query, source",
    [
        ("How long does shipping take?", "shipping_policy"),
        ("What is your return policy?", "returns_policy"),
        ("How long is the warranty?", "warranty_policy"),
    ],
)
def test_retriever_picks_the_right_document(query, source):
    docs = build_retriever().invoke(query)
    assert docs and docs[0].metadata["source"] == source


def test_retriever_returns_nothing_for_unrelated_query():
    assert build_retriever().invoke("quantum chromodynamics lecture") == []
