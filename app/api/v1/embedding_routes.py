from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import EmbeddingService

router = APIRouter()

embedding_service = EmbeddingService()


class EmbeddingRequest(BaseModel):
    text: str


@router.post("/embed")
def create_embedding(request: EmbeddingRequest):

    if not request.text.strip():
        return {
            "error": "Text cannot be empty."
        }

    embedding = embedding_service.generate_embedding(
        request.text
    )

    return {
        "text": request.text,
        "dimension": len(embedding),
        "embedding": embedding
    }