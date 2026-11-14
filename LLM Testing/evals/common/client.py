"""Small HTTP client for the agent under test."""
import os
from dataclasses import dataclass, field
from typing import Dict, List

import httpx

DEFAULT_URL = "http://127.0.0.1:8000"


@dataclass
class AgentReply:
    content: str
    tools_called: List[str] = field(default_factory=list)
    retrieval_context: List[str] = field(default_factory=list)
    latency_ms: float = 0.0
    variant: str = ""


class AgentClient:
    def __init__(self, base_url: str = None, timeout: float = 15.0):
        self.base_url = (base_url or os.getenv("AGENT_URL") or DEFAULT_URL).rstrip("/")
        self.http = httpx.Client(timeout=timeout)

    def chat(self, messages: List[Dict[str, str]]) -> AgentReply:
        response = self.http.post(f"{self.base_url}/v1/chat/completions", json={"messages": messages})
        response.raise_for_status()
        body = response.json()
        meta = body.get("x_agent", {})
        return AgentReply(
            content=body["choices"][0]["message"]["content"],
            tools_called=[t["name"] for t in meta.get("tools_called", [])],
            retrieval_context=meta.get("retrieval_context", []),
            latency_ms=meta.get("latency_ms", 0.0),
            variant=meta.get("variant", ""),
        )

    def health(self) -> dict:
        response = self.http.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
