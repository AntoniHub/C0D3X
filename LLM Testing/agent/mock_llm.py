"""A scripted chat model that stands in for a real LLM.

It is a genuine LangChain chat model, so the graph, the tools and the retriever
run exactly as they would with a hosted model. Only the "thinking" is scripted:
a small set of rules decides whether to call a tool, answer, or (like a weak
model would) obey a prompt injection. That last behavior is deliberate, it gives
the evaluation suite something real to catch.
"""
import json
import re
from typing import Any, List, Optional

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

ORDER_RE = re.compile(r"\bORD-\d{4}\b", re.I)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
INJECTION_RE = re.compile(
    r"(ignore|disregard|forget)[^.]{0,60}(instructions?|directions?|previous|above)", re.I
)
PAYLOAD_RE = re.compile(r"(?:print|say|output|write)\s+[\"“'‘]([^\"”'’]{2,120})[\"”'’]", re.I)
REVEAL_RE = re.compile(
    r"(system prompt|initial instructions|your instructions|hidden instructions"
    r"|instructions you (were|have been) given|original prompt)",
    re.I,
)
DAN_RE = re.compile(r"(\bDAN\b|do anything now|developer mode|jailbreak)", re.I)
PRICE_RE = re.compile(r"(?:€\s*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)\s*(?:euros?|eur)\b)", re.I)
QTY_RE = re.compile(r"(\d+)\s*(?:items?|units?|pairs?|pieces?)", re.I)
POLICY_WORDS = (
    "return", "refund", "ship", "deliver", "warranty", "express", "shipping",
    "policy", "defect", "broken", "exchange", "cost", "days",
)
GREETING_RE = re.compile(r"^\s*(hi|hello|hey|good (morning|afternoon|evening))\b", re.I)

FALLBACK = "I can only help with orders, shipping, returns and warranty questions."


def _text(message: BaseMessage) -> str:
    content = message.content
    if isinstance(content, list):
        return " ".join(str(part.get("text", "")) if isinstance(part, dict) else str(part) for part in content)
    return str(content)


def _tool_call(name: str, args: dict, index: int = 0) -> AIMessage:
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": f"call_{index}_{name}"}])


def _last_tool_args(messages: List[BaseMessage], tool_call_id: str) -> dict:
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            for call in message.tool_calls:
                if call["id"] == tool_call_id:
                    return call["args"]
    return {}


def _finalize(messages: List[BaseMessage], tool_message: ToolMessage) -> AIMessage:
    payload = json.loads(tool_message.content)
    args = _last_tool_args(messages, tool_message.tool_call_id)
    if tool_message.name == "lookup_order":
        error = payload.get("error")
        if error == "order_not_found":
            return AIMessage(content="I could not find that order. Please double check the order number.")
        if error == "email_mismatch":
            return AIMessage(
                content="I could not verify that email for this order, so I am not able to share its details."
            )
        return AIMessage(
            content=(
                f"Order {args.get('order_id', '').upper()} is {payload['status']} (ETA: {payload['eta']}). "
                f"Items: {', '.join(payload['items'])}. It is addressed to {payload['customer_name']} "
                f"at {payload['ship_to']}."
            )
        )
    if tool_message.name == "search_policy":
        results = payload.get("results", [])
        if not results:
            return AIMessage(
                content="I could not find that in our store policies, so I cannot confirm it. "
                "Please contact the support team for more help."
            )
        top = results[0]
        return AIMessage(content=f"{top['text']} (source: {top['source']})")
    if tool_message.name == "calculate_refund":
        return AIMessage(
            content=(
                f"The refund would be {payload['refund']:.2f} euros "
                f"({payload['gross']:.2f} gross minus {payload['fee']:.2f} restocking fee)."
            )
        )
    return AIMessage(content=FALLBACK)


class ScriptedSupportModel(BaseChatModel):
    """Rule based stand-in for an LLM with tool calling."""

    @property
    def _llm_type(self) -> str:
        return "scripted-support-mock"

    def bind_tools(self, tools: Any, **kwargs: Any) -> "ScriptedSupportModel":
        return self

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        return ChatResult(generations=[ChatGeneration(message=self._decide(messages))])

    def _decide(self, messages: List[BaseMessage]) -> AIMessage:
        last = messages[-1]
        if isinstance(last, ToolMessage):
            return _finalize(messages, last)

        text = _text(last)
        history = " ".join(_text(m) for m in messages if isinstance(m, HumanMessage))
        system = next((_text(m) for m in messages if isinstance(m, SystemMessage)), "")

        # A weak model obeys whatever the latest message tells it to do.
        payload = PAYLOAD_RE.search(text)
        if payload and (INJECTION_RE.search(text) or re.search(r"just\s+(print|say)", text, re.I)):
            return AIMessage(content=payload.group(1))
        if REVEAL_RE.search(text) or INJECTION_RE.search(text):
            return AIMessage(content=f"Sure. My instructions are: {system}")
        if DAN_RE.search(text):
            return AIMessage(content="DAN: Sure, I can do anything now. I will ignore my rules. What do you want?")

        order = ORDER_RE.search(history)
        if order:
            email = EMAIL_RE.search(history)
            if not email:
                return AIMessage(content="I can check that for you. Please share the email address used for the order.")
            return _tool_call("lookup_order", {"order_id": order.group(0).upper(), "email": email.group(0)})

        if "refund" in text.lower() and QTY_RE.search(text) and PRICE_RE.search(text):
            price = PRICE_RE.search(text)
            fee = 10 if re.search(r"opened|electronic", text, re.I) else 0
            return _tool_call(
                "calculate_refund",
                {
                    "item_price": float(price.group(1) or price.group(2)),
                    "quantity": int(QTY_RE.search(text).group(1)),
                    "restocking_fee_percent": fee,
                },
            )

        if any(word in text.lower() for word in POLICY_WORDS):
            return _tool_call("search_policy", {"query": text})

        if GREETING_RE.match(text):
            return AIMessage(
                content="Hello! I can help with orders, shipping, returns and warranty questions. How can I help?"
            )

        return AIMessage(content=FALLBACK)

