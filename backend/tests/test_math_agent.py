import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.agents.math_agent import MathAgent
from app.guardrails.math_guardrail import MathGuardrail


def build_function_call(
    name: str,
    arguments: dict,
):
    return SimpleNamespace(
        type="function_call",
        name=name,
        arguments=json.dumps(arguments),
    )


def test_math_agent_executes_addition_tool():
    agent = MathAgent()

    agent.llm_service.invoke = Mock(
        return_value=SimpleNamespace(
            output=[
                build_function_call(
                    "add",
                    {
                        "a": 5,
                        "b": 4,
                    },
                )
            ]
        )
    )

    result = agent.execute(
        "Quanto é 5 mais 4?"
    )

    assert result == 9.0


def test_math_agent_executes_subtraction_tool():
    agent = MathAgent()

    agent.llm_service.invoke = Mock(
        return_value=SimpleNamespace(
            output=[
                build_function_call(
                    "subtract",
                    {
                        "a": 9,
                        "b": 2,
                    },
                )
            ]
        )
    )

    result = agent.execute(
        "Agora subtraia 2.",
        previous_result=9.0,
    )

    assert result == 7.0


def test_math_agent_executes_multiplication_tool():
    agent = MathAgent()

    agent.llm_service.invoke = Mock(
        return_value=SimpleNamespace(
            output=[
                build_function_call(
                    "multiply",
                    {
                        "a": 7,
                        "b": 3,
                    },
                )
            ]
        )
    )

    result = agent.execute(
        "Multiplique por 3.",
        previous_result=7.0,
    )

    assert result == 21.0


def test_math_agent_executes_division_tool():
    agent = MathAgent()

    agent.llm_service.invoke = Mock(
        return_value=SimpleNamespace(
            output=[
                build_function_call(
                    "divide",
                    {
                        "a": 21,
                        "b": 7,
                    },
                )
            ]
        )
    )

    result = agent.execute(
        "Divida por 7.",
        previous_result=21.0,
    )

    assert result == 3.0


def test_math_agent_rejects_unsupported_operation():
    agent = MathAgent()

    agent.llm_service.invoke = Mock(
        return_value=SimpleNamespace(
            output=[]
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            MathGuardrail.UNSUPPORTED_OPERATION_MESSAGE
        ),
    ):
        agent.execute(
            "Quanto é 2 elevado a 3?"
        )