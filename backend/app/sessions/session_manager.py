from uuid import UUID, uuid4

from app.orchestrators.chat_orchestrator import ChatOrchestrator


class SessionManager:
    def __init__(self):
        self.sessions: dict[UUID, ChatOrchestrator] = {}

    def create_session(
        self,
    ) -> tuple[UUID, ChatOrchestrator]:
        session_id = uuid4()
        orchestrator = ChatOrchestrator()

        self.sessions[session_id] = orchestrator

        return session_id, orchestrator

    def get_session(
        self,
        session_id: UUID,
    ) -> ChatOrchestrator | None:
        return self.sessions.get(session_id)

    def delete_session(
        self,
        session_id: UUID,
    ) -> bool:
        if session_id not in self.sessions:
            return False

        del self.sessions[session_id]

        return True
