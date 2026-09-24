from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.agents.writer_agent import WriterAgent


def test_writer_agent_returns_formatted_response():
    agent = WriterAgent()

    agent.llm_service.invoke = Mock(
        return_value=SimpleNamespace(
            output_text="O resultado final é 9.0."
        )
    )

    response = agent.execute(
        user_message="Quanto é 5 mais 4?",
        result=9.0,
    )

    assert response == "O resultado final é 9.0."


def test_writer_agent_removes_extra_whitespace():
    agent = WriterAgent()

    agent.llm_service.invoke = Mock(
        return_value=SimpleNamespace(
            output_text="  O resultado é 7.0.  "
        )
    )

    response = agent.execute(
        user_message="Agora subtraia 2.",
        result=7.0,
    )

    assert response == "O resultado é 7.0."


def test_writer_agent_rejects_empty_response():
    agent = WriterAgent()

    agent.llm_service.invoke = Mock(
        return_value=SimpleNamespace(
            output_text=""
        )
    )

    with pytest.raises(
        ValueError,
        match="The Writer Agent did not produce a response.",
    ):
        agent.execute(
            user_message="Quanto é 5 mais 4?",
            result=9.0,
        )