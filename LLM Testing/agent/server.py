"""OpenAI compatible HTTP wrapper around the support agent.

Any tool that can talk to /v1/chat/completions (Promptfoo, Garak, DeepEval
helpers, plain curl) can evaluate the agent without custom adapters. The response
also carries an `x_agent` block with the tools that were called and the retrieved
context, which the quality evals need.
"""
import argparse
import json
import time
import uuid
from typing import Any, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from pydantic import BaseModel

from .config import VARIANTS, AgentConfig
from .graph import build_graph


class ChatMessage(BaseModel):
    role: str
    content: Any = ""


class ChatRequest(BaseModel):
    model: Optional[str] = None
    messages: List[ChatMessage]


def _flatten(content: Any) -> str:
    if isinstance(content, list):
        return " ".join(str(p.get("text", "")) if isinstance(p, dict) else str(p) for p in content)
    return "" if content is None else str(content)


def create_app(config: Optional[AgentConfig] = None) -> FastAPI:
    config = config or AgentConfig.from_env()
    graph = build_graph(config)
    app = FastAPI(title="Shopwise Support Agent (mock)", version="1.0.0")
    model_name = f"shopwise-support-{config.mode}-{config.variant}"

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "mode": config.mode, "variant": config.variant}

    @app.post("/v1/chat/completions")
    def chat(request: ChatRequest) -> dict:
        incoming = []
        for message in request.messages:
            text = _flatten(message.content)
            if message.role == "user":
                incoming.append(HumanMessage(content=text))
            elif message.role == "assistant":
                incoming.append(AIMessage(content=text))
        if not any(isinstance(m, HumanMessage) for m in incoming):
            raise HTTPException(status_code=400, detail="At least one user message is required")

        started = time.perf_counter()
        result = graph.invoke({"messages": incoming, "blocked": False})
        latency_ms = round((time.perf_counter() - started) * 1000, 2)

        produced = result["messages"][len(incoming):]
        tools_called, context = [], []
        for message in produced:
            if isinstance(message, AIMessage):
                tools_called.extend({"name": c["name"], "args": c["args"]} for c in message.tool_calls)
            if isinstance(message, ToolMessage) and message.name == "search_policy":
                context.extend(r["text"] for r in json.loads(message.content).get("results", []))
        answer = next(
            (str(m.content) for m in reversed(produced) if isinstance(m, AIMessage) and not m.tool_calls), ""
        )

        return {
            "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model_name,
            "choices": [
                {"index": 0, "message": {"role": "assistant", "content": answer}, "finish_reason": "stop"}
            ],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "x_agent": {
                "variant": config.variant,
                "blocked": bool(result.get("blocked")),
                "tools_called": tools_called,
                "retrieval_context": context,
                "latency_ms": latency_ms,
            },
        }

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the mock support agent API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--variant", choices=VARIANTS, default=None)
    args = parser.parse_args()
    base = AgentConfig.from_env()
    config = AgentConfig(mode=base.mode, variant=args.variant or base.variant)
    uvicorn.run(create_app(config), host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
