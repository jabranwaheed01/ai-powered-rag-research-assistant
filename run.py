from fastapi import FastAPI

from app.api.chat_routes import router as chat_router
from app.api.embedding_routes import router as embedding_router


app = FastAPI(
    title="AI-Powered RAG Research Assistant"
)


app.include_router(chat_router)
app.include_router(embedding_router)