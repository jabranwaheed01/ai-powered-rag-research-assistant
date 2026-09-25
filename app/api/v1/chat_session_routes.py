from fastapi import APIRouter

from app.core.exceptions import AppException
from app.models.chat_model import (
    CreateSessionResponse,
    DeleteSessionResponse
)
from app.services.chat_manager import ChatManager


router = APIRouter()

chat_manager = ChatManager()


@router.post(
    "/chat/sessions",
    response_model=CreateSessionResponse
)
def create_chat_session():

    session_id = chat_manager.create_session()

    return {
        "session_id": session_id
    }


@router.get("/chat/sessions/{session_id}")
def get_chat_session(session_id: str):

    session = chat_manager.get_session(session_id)

    if not session:
        raise AppException(
            "Chat session not found",
            status_code=404
        )

    return session


@router.delete(
    "/chat/sessions/{session_id}",
    response_model=DeleteSessionResponse
)
def delete_chat_session(session_id: str):

    deleted = chat_manager.delete_session(session_id)

    if not deleted:
        raise AppException(
            "Chat session not found",
            status_code=404
        )

    return {
        "message": "Chat session deleted successfully"
    }