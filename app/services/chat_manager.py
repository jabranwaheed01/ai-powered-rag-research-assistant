
import logging
import uuid
from datetime import datetime, timezone

from app.services.mongodb_service import MongoDBService


logger = logging.getLogger(__name__)


class ChatManager:

    def __init__(self):

        logger.info(
            "Initializing ChatManager"
        )

        self.mongodb = MongoDBService()
        self.collection = self.mongodb.get_collection(
            "chat_sessions"
        )

        logger.info(
            "ChatManager initialized successfully"
        )

    def create_session(self):

        session_id = str(uuid.uuid4())

        logger.info(
            "Creating chat session | session_id=%s",
            session_id
        )

        session = {
            "session_id": session_id,
            "created_at": datetime.now(timezone.utc),
            "messages": []
        }

        try:

            result = self.collection.insert_one(
                session
            )

            logger.info(
                "Chat session inserted | inserted_id=%s",
                result.inserted_id
            )

            saved_session = self.collection.find_one(
                {"session_id": session_id}
            )

            if saved_session:

                logger.info(
                    "Chat session verified | session_id=%s",
                    session_id
                )

            else:

                logger.warning(
                    "Chat session could not be verified | session_id=%s",
                    session_id
                )

            return session_id

        except Exception:

            logger.exception(
                "Failed to create chat session | session_id=%s",
                session_id
            )

            raise

    def add_message(
        self,
        session_id,
        query,
        answer,
        sources
    ):

        logger.info(
            "Adding message to chat session | session_id=%s",
            session_id
        )

        message = {
            "query": query,
            "answer": answer,
            "sources": sources,
            "timestamp": datetime.now(timezone.utc)
        }

        try:

            result = self.collection.update_one(
                {"session_id": session_id},
                {"$push": {"messages": message}}
            )

            if result.matched_count == 0:

                logger.warning(
                    "Session not found while adding message | session_id=%s",
                    session_id
                )

                return

            logger.info(
                "Message saved successfully | session_id=%s",
                session_id
            )

        except Exception:

            logger.exception(
                "Failed to save message | session_id=%s",
                session_id
            )

            raise

    def get_session(self, session_id):

        logger.info(
            "Fetching chat session | session_id=%s",
            session_id
        )

        try:

            session = self.collection.find_one(
                {"session_id": session_id},
                {"_id": 0}
            )

            if session:

                logger.info(
                    "Chat session found | session_id=%s",
                    session_id
                )

            else:

                logger.warning(
                    "Chat session not found | session_id=%s",
                    session_id
                )

            return session

        except Exception:

            logger.exception(
                "Failed to fetch chat session | session_id=%s",
                session_id
            )

            raise

    def delete_session(self, session_id):

        logger.info(
            "Deleting chat session | session_id=%s",
            session_id
        )

        try:

            result = self.collection.delete_one(
                {"session_id": session_id}
            )

            deleted = result.deleted_count > 0

            if deleted:

                logger.info(
                    "Chat session deleted | session_id=%s",
                    session_id
                )

            else:

                logger.warning(
                    "Chat session not found for deletion | session_id=%s",
                    session_id
                )

            return deleted

        except Exception:

            logger.exception(
                "Failed to delete chat session | session_id=%s",
                session_id
            )

            raise