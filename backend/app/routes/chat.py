from fastapi import APIRouter, HTTPException, status

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.sessions.session_manager import SessionManager


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

session_manager = SessionManager()


@router.post(
    "/message",
    response_model=ChatResponse,
)
def send_message(
    payload: ChatRequest,
) -> ChatResponse:
    if payload.session_id is None:
        session_id, orchestrator = (
            session_manager.create_session()
        )
    else:
        session_id = payload.session_id
        orchestrator = session_manager.get_session(
            session_id
        )

        if orchestrator is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found.",
            )

    response = orchestrator.process(
        payload.message
    )

    return ChatResponse(
        session_id=session_id,
        response=response,
    )


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session(
    session_id: UUID,
) -> None:
    deleted = session_manager.delete_session(
        session_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )
