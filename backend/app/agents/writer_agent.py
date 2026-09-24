from app.agents.prompts.writer_prompt import WRITER_PROMPT
from app.guardrails.write_guardrail import WriterGuardrail
from app.services.llm_service import LLMService


class WriterAgent:
    def __init__(self):
        self.llm_service = LLMService()

    def execute(
        self,
        user_message: str,
        result: float,
    ) -> str:
        messages = [
            {
                "role": "system",
                "content": WRITER_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    "Write the final response using the information below.\n\n"
                    f"User language/context:\n{user_message}\n\n"
                    "Final verified result — do not calculate again:\n"
                    f"{result}"
                ),
            },
        ]

        response = self.llm_service.invoke(
            messages=messages,
        )

        return WriterGuardrail.validate(
            response.output_text
        )