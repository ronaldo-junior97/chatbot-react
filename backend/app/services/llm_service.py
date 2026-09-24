import inspect
from collections.abc import Callable

from openai import OpenAI

from app.config.settings import settings


class LLMService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
        )
        self.model = settings.model_name

    def invoke(
        self,
        messages: list,
        tools: list[Callable] | None = None,
    ):
        openai_tools = None

        if tools:
            openai_tools = [
                self._build_tool_schema(tool)
                for tool in tools
            ]

        return self.client.responses.create(
            model=self.model,
            input=messages,
            tools=openai_tools,
        )

    @staticmethod
    def _build_tool_schema(
        tool: Callable,
    ) -> dict:
        signature = inspect.signature(tool)

        properties = {}
        required = []

        for parameter_name in signature.parameters:
            properties[parameter_name] = {
                "type": "number",
            }

            required.append(parameter_name)

        return {
            "type": "function",
            "name": tool.__name__,
            "description": inspect.getdoc(tool) or "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
            "strict": True,
        }