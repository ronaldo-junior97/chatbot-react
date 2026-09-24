from unittest.mock import Mock

from app.orchestrators.chat_orchestrator import ChatOrchestrator


def test_orchestrator_processes_message():
    orchestrator = ChatOrchestrator()

    orchestrator.math_agent.execute = Mock(
        return_value=9.0
    )

    orchestrator.writer_agent.execute = Mock(
        return_value="O resultado é 9.0."
    )

    response = orchestrator.process(
        "Quanto é 5 mais 4?"
    )

    assert response == "O resultado é 9.0."

    assert orchestrator.memory.get_last_result() == 9.0

    assert orchestrator.memory.get_messages() == [
        {
            "role": "user",
            "content": "Quanto é 5 mais 4?",
        },
        {
            "role": "assistant",
            "content": "O resultado é 9.0.",
        },
    ]


def test_orchestrator_uses_previous_result():
    orchestrator = ChatOrchestrator()

    orchestrator.memory.set_last_result(9.0)

    orchestrator.math_agent.execute = Mock(
        return_value=7.0
    )

    orchestrator.writer_agent.execute = Mock(
        return_value="O resultado é 7.0."
    )

    response = orchestrator.process(
        "Agora subtraia 2."
    )

    assert response == "O resultado é 7.0."

    orchestrator.math_agent.execute.assert_called_once_with(
        message="Agora subtraia 2.",
        conversation_history=[],
        previous_result=9.0,
    )

    assert orchestrator.memory.get_last_result() == 7.0


def test_orchestrator_handles_math_error():
    orchestrator = ChatOrchestrator()

    orchestrator.math_agent.execute = Mock(
        side_effect=ValueError(
            "Unsupported operation."
        )
    )

    orchestrator.writer_agent.execute = Mock()

    response = orchestrator.process(
        "Quanto é 2 elevado a 3?"
    )

    assert response == "Unsupported operation."

    orchestrator.writer_agent.execute.assert_not_called()

    assert orchestrator.memory.get_messages() == [
        {
            "role": "user",
            "content": "Quanto é 2 elevado a 3?",
        },
        {
            "role": "assistant",
            "content": "Unsupported operation.",
        },
    ]