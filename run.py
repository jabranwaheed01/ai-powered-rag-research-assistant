# # from fastapi import FastAPI

# # from app.api.chat_routes import router as chat_router
# # from app.api.embedding_routes import router as embedding_router



# # app = FastAPI(
# #     title="AI-Powered RAG Research Assistant"
# # )


# # app.include_router(chat_router)
# # app.include_router(embedding_router)




# from fastapi import FastAPI

# from app.api.chat_routes import router as chat_router
# from app.api.embedding_routes import router as embedding_router
# from app.core.logging import setup_logging
# from app.core.exceptions import AppException
# from app.core.exception_handlers import (
#     app_exception_handler,
#     general_exception_handler
# )


# setup_logging()


# app = FastAPI(
#     title="AI-Powered RAG Research Assistant"
# )


# app.add_exception_handler(
#     AppException,
#     app_exception_handler
# )

# app.add_exception_handler(
#     Exception,
#     general_exception_handler
# )


# app.include_router(chat_router)
# app.include_router(embedding_router)



from fastapi import FastAPI

from app.api.v1.chat_routes import router as chat_router
from app.api.v1.embedding_routes import router as embedding_router
from app.api.v1.health_routes import router as health_router
from app.api.v1.chat_session_routes import router as chat_session_router

from app.core.logging import setup_logging
from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    general_exception_handler
)


setup_logging()


app = FastAPI(
    title="AI-Powered RAG Research Assistant"
)


app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)


app.include_router(
    chat_router,
    prefix="/api/v1"
)

app.include_router(
    embedding_router,
    prefix="/api/v1"
)

app.include_router(
    health_router,
    prefix="/api/v1"
)
app.include_router(
    chat_session_router,
    prefix="/api/v1"
)