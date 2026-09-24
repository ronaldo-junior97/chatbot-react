import json

from app.agents.prompts.math_prompt import MATH_PROMPT
from app.guardrails.math_guardrail import MathGuardrail
from app.services.llm_service import LLMService
from app.tools.addition_tool import add
from app.tools.division_tool import divide
from app.tools.multiplication_tool import multiply
from app.tools.subtraction_tool import subtract


class MathAgent:
    def __init__(self):
        self.llm_service = LLMService()

        self.tools = [
            add,
            subtract,
            multiply,
            divide,
        ]

        self.available_tools = {
            "add": add,
            "subtract": subtract,
            "multiply": multiply,
            "divide": divide,
        }

    def execute(
        self,
        message: str,
        conversation_history: list | None = None,
        previous_result: float | None = None,
    ) -> float:
        messages = [
            {
                "role": "system",
                "content": MATH_PROMPT,
            }
        ]

        if conversation_history:
            messages.extend(conversation_history)

        if previous_result is not None:
            messages.append(
                {
                    "role": "system",
                    "content": (
                        "The verified result of the previous "
                        f"mathematical operation is {previous_result}. "
                        "Use this value only if the user's new request "
                        "depends on the previous result."
                    ),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        response = self.llm_service.invoke(
            messages=messages,
            tools=self.tools,
        )

        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            raise ValueError(
                MathGuardrail.unsupported_operation()
            )

        last_result = None

        for function_call in function_calls:
            tool_name = function_call.name
            tool_function = self.available_tools.get(
                tool_name
            )

            if tool_function is None:
                raise ValueError(
                    MathGuardrail.unsupported_operation()
                )

            try:
                arguments = json.loads(
                    function_call.arguments
                )

                result = tool_function(
                    **arguments
                )
            except (
                ValueError,
                TypeError,
                json.JSONDecodeError,
            ):
                raise ValueError(
                    MathGuardrail.invalid_calculation()
                )

            last_result = float(result)

        if last_result is None:
            raise ValueError(
                MathGuardrail.invalid_calculation()
            )

        return last_result