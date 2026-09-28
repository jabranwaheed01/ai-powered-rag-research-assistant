
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.chat_model import AskRequest, AskResponse
from app.services.chatbot_service import ChatbotService


router = APIRouter()

chatbot = ChatbotService()


@router.post(
    "/ask",
    response_model=AskResponse
)
def ask_question(request: AskRequest):

    result = chatbot.ask(
        query=request.query,
        top_k=request.top_k,
        topic=request.topic,
        year=request.year,
        mode=request.mode,
        session_id=request.session_id
    )

    return result


@router.post("/ask/stream")
def ask_question_stream(request: AskRequest):

    return StreamingResponse(
        chatbot.ask_stream(
            query=request.query,
            top_k=request.top_k,
            topic=request.topic,
            year=request.year,
            session_id=request.session_id,
            mode=request.mode
        ),
        media_type="text/plain"
    )