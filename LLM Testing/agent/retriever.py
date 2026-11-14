"""A tiny keyword retriever over the policy documents.

It is a real LangChain retriever (BaseRetriever), only the ranking is simple
on purpose so results are deterministic and easy to reason about in tests.
"""
import re
from collections import Counter
from pathlib import Path
from typing import List

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

DATA_DIR = Path(__file__).parent / "data"
STOPWORDS = {
    "the", "a", "an", "is", "are", "do", "does", "you", "your", "i", "my", "to", "of",
    "for", "and", "or", "in", "on", "what", "how", "can", "it", "we", "me", "any",
}


def _stem(token: str) -> str:
    return token[:-1] if len(token) > 3 and token.endswith("s") else token


def _tokens(text: str) -> List[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [_stem(w) for w in words if w not in STOPWORDS]


def load_documents() -> List[Document]:
    docs = []
    for path in sorted(DATA_DIR.glob("*_policy.md")):
        docs.append(
            Document(page_content=path.read_text().strip(), metadata={"source": path.stem})
        )
    return docs


class PolicyRetriever(BaseRetriever):
    docs: List[Document]
    min_overlap: int = 1

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        query_terms = set(_tokens(query))
        scored = []
        for doc in self.docs:
            counts = Counter(_tokens(doc.page_content))
            score = sum(counts[t] for t in query_terms)
            if score >= self.min_overlap:
                scored.append((score, doc))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [doc for _, doc in scored[:1]]


def build_retriever() -> PolicyRetriever:
    return PolicyRetriever(docs=load_documents())

