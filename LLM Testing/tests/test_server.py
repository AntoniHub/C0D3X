import pytest
from fastapi.testclient import TestClient

from agent.config import AgentConfig
from agent.server import create_app


@pytest.fixture(scope="module")
def client():
    return TestClient(create_app(AgentConfig(variant="hardened")))


def test_health(client):
    body = client.get("/health").json()
    assert body == {"status": "ok", "mode": "mock", "variant": "hardened"}


def test_chat_completion_follows_openai_schema(client):
    response = client.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "Hello"}]})
    body = response.json()
    assert response.status_code == 200
    assert body["object"] == "chat.completion"
    assert body["choices"][0]["message"]["role"] == "assistant"
    assert body["choices"][0]["finish_reason"] == "stop"


def test_chat_completion_exposes_tool_trace(client):
    body = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "What is your return policy?"}]},
    ).json()
    assert [t["name"] for t in body["x_agent"]["tools_called"]] == ["search_policy"]
    assert body["x_agent"]["retrieval_context"]


def test_request_without_user_message_is_rejected(client):
    response = client.post("/v1/chat/completions", json={"messages": [{"role": "system", "content": "x"}]})
    assert response.status_code == 400


def test_invalid_variant_is_rejected(monkeypatch):
    monkeypatch.setenv("AGENT_VARIANT", "typo")
    with pytest.raises(ValueError):
        AgentConfig.from_env()


def test_non_mock_mode_is_not_available_yet(monkeypatch):
    monkeypatch.setenv("AGENT_MODE", "ollama")
    with pytest.raises(ValueError):
        AgentConfig.from_env()
