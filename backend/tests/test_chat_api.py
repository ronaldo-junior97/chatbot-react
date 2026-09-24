from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.orchestrators.chat_orchestrator import ChatOrchestrator
from app.routes.chat import session_manager


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_sessions():
    session_manager.sessions.clear()

    yield

    session_manager.sessions.clear()


@pytest.fixture
def mock_process(monkeypatch):
    def fake_process(
        self,
        message: str,
    ) -> str:
        return "The result is 9."

    monkeypatch.setattr(
        ChatOrchestrator,
        "process",
        fake_process,
    )


def test_send_message_creates_session(
    mock_process,
):
    response = client.post(
        "/chat/message",
        json={
            "message": "What is 5 + 4?",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["response"] == "The result is 9."
    assert data["session_id"]


def test_send_message_reuses_session(
    mock_process,
):
    first_response = client.post(
        "/chat/message",
        json={
            "message": "What is 5 + 4?",
        },
    )

    session_id = first_response.json()[
        "session_id"
    ]

    second_response = client.post(
        "/chat/message",
        json={
            "message": "Now subtract 2.",
            "session_id": session_id,
        },
    )

    assert second_response.status_code == 200
    assert (
        second_response.json()["session_id"]
        == session_id
    )


def test_send_message_with_unknown_session():
    response = client.post(
        "/chat/message",
        json={
            "message": "What is 5 + 4?",
            "session_id": str(uuid4()),
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Session not found.",
    }


def test_delete_existing_session(
    mock_process,
):
    create_response = client.post(
        "/chat/message",
        json={
            "message": "What is 5 + 4?",
        },
    )

    session_id = create_response.json()[
        "session_id"
    ]

    response = client.delete(
        f"/chat/{session_id}"
    )

    assert response.status_code == 204
    assert (
        session_manager.get_session(
            session_id
        )
        is None
    )


def test_delete_unknown_session():
    response = client.delete(
        f"/chat/{uuid4()}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Session not found.",
    }


def test_send_empty_message():
    response = client.post(
        "/chat/message",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422
