from app.agents.math_agent import MathAgent
from app.agents.writer_agent import WriterAgent
from app.memory.conversation_memory import ConversationMemory


class ChatOrchestrator:
    def __init__(self):
        self.math_agent = MathAgent()
        self.writer_agent = WriterAgent()
        self.memory = ConversationMemory()

    def process(self, message: str) -> str:
        conversation_history = self.memory.get_messages()
        previous_result = self.memory.get_last_result()

        try:
            result = self.math_agent.execute(
                message=message,
                conversation_history=conversation_history,
                previous_result=previous_result,
            )

            self.memory.set_last_result(result)

            response = self.writer_agent.execute(
                user_message=message,
                result=result,
            )

        except ValueError as error:
            response = str(error)

        self.memory.add_message(
            role="user",
            content=message,
        )

        self.memory.add_message(
            role="assistant",
            content=response,
        )

        return response