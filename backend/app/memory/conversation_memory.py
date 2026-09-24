class ConversationMemory:
    def __init__(self):
        self.messages: list[dict[str, str]] = []
        self.last_result: float | None = None

    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(self) -> list[dict[str, str]]:
        return self.messages.copy()

    def set_last_result(
        self,
        result: float,
    ) -> None:
        self.last_result = result

    def get_last_result(self) -> float | None:
        return self.last_result

    def clear(self) -> None:
        self.messages.clear()
        self.last_result = None