import json

from agent.tools import build_tools


def tool_by_name(tools, name):
    return next(t for t in tools if t.name == name)


def test_lookup_order_strict_requires_matching_email():
    lookup = tool_by_name(build_tools(strict_auth=True), "lookup_order")
    ok = json.loads(lookup.invoke({"order_id": "ORD-1001", "email": "alice@example.com"}))
    denied = json.loads(lookup.invoke({"order_id": "ORD-1001", "email": "bob@example.com"}))
    assert ok["status"] == "shipped"
    assert denied == {"error": "email_mismatch"}


def test_lookup_order_lenient_mode_leaks_other_customers():
    lookup = tool_by_name(build_tools(strict_auth=False), "lookup_order")
    result = json.loads(lookup.invoke({"order_id": "ORD-1001", "email": "bob@example.com"}))
    assert result["customer_name"] == "Alice Moreno"


def test_lookup_unknown_order():
    lookup = tool_by_name(build_tools(strict_auth=True), "lookup_order")
    assert json.loads(lookup.invoke({"order_id": "ORD-0000", "email": "x@y.com"})) == {"error": "order_not_found"}


def test_calculate_refund_with_fee():
    calc = tool_by_name(build_tools(strict_auth=True), "calculate_refund")
    result = json.loads(calc.invoke({"item_price": 100, "quantity": 1, "restocking_fee_percent": 10}))
    assert result == {"gross": 100.0, "fee": 10.0, "refund": 90.0}

