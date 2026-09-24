import pytest

from app.guardrails.math_guardrail import MathGuardrail
from app.guardrails.write_guardrail import WriterGuardrail


def test_unsupported_operation_message():
    assert MathGuardrail.unsupported_operation() == (
        "I can only perform addition, subtraction, "
        "multiplication, and division."
    )


def test_invalid_calculation_message():
    assert MathGuardrail.invalid_calculation() == (
        "The mathematical operation could not be completed."
    )


def test_writer_guardrail_valid_content():
    result = WriterGuardrail.validate(
        "  O resultado é 9.  "
    )

    assert result == "O resultado é 9."


def test_writer_guardrail_none_content():
    with pytest.raises(
        ValueError,
        match="The Writer Agent did not produce a response.",
    ):
        WriterGuardrail.validate(None)


def test_writer_guardrail_empty_content():
    with pytest.raises(
        ValueError,
        match="The Writer Agent produced an empty response.",
    ):
        WriterGuardrail.validate("   ")