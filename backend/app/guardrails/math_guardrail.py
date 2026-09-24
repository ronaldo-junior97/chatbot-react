class MathGuardrail:
    UNSUPPORTED_OPERATION_MESSAGE = (
        "I can only perform addition, subtraction, "
        "multiplication, and division."
    )

    INVALID_CALCULATION_MESSAGE = (
        "The mathematical operation could not be completed."
    )

    @classmethod
    def unsupported_operation(cls) -> str:
        return cls.UNSUPPORTED_OPERATION_MESSAGE

    @classmethod
    def invalid_calculation(cls) -> str:
        return cls.INVALID_CALCULATION_MESSAGE