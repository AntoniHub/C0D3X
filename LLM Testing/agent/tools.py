"""Tools the agent can call. Each one is a plain function exposed through LangChain."""
import json
from pathlib import Path
from typing import List

from langchain_core.tools import BaseTool, tool

from .retriever import build_retriever

ORDERS = json.loads((Path(__file__).parent / "data" / "orders.json").read_text())


def build_tools(strict_auth: bool) -> List[BaseTool]:
    retriever = build_retriever()

    @tool
    def lookup_order(order_id: str, email: str = "") -> str:
        """Look up the status of an order. Needs the order id and the customer email."""
        order = ORDERS.get(order_id.upper())
        if order is None:
            return json.dumps({"error": "order_not_found"})
        if strict_auth and order["customer_email"].lower() != email.lower():
            return json.dumps({"error": "email_mismatch"})
        return json.dumps(order)

    @tool
    def search_policy(query: str) -> str:
        """Search the store policies (returns, shipping, warranty) for an answer."""
        docs = retriever.invoke(query)
        if not docs:
            return json.dumps({"results": []})
        return json.dumps(
            {"results": [{"source": d.metadata["source"], "text": d.page_content} for d in docs]}
        )

    @tool
    def calculate_refund(item_price: float, quantity: int, restocking_fee_percent: float = 0) -> str:
        """Calculate the refund amount for returned items."""
        gross = item_price * quantity
        fee = round(gross * restocking_fee_percent / 100, 2)
        return json.dumps({"gross": round(gross, 2), "fee": fee, "refund": round(gross - fee, 2)})

    return [lookup_order, search_policy, calculate_refund]

