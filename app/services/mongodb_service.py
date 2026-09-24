

import logging

from pymongo import MongoClient

from app.core.config import settings


logger = logging.getLogger(__name__)


class MongoDBService:

    def __init__(self):
        logger.info("Initializing MongoDBService")

        if not settings.MONGODB_URI:
            raise ValueError("MONGODB_URI is missing in .env")

        self.mongo_uri = settings.MONGODB_URI
        self.database_name = getattr(
            settings,
            "MONGODB_DB",
            "rag_research_assistant"
        )

        try:
            self.client = MongoClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=5000
            )

            self.db = self.client[self.database_name]

            logger.info(
                "MongoDBService initialized | database=%s",
                self.database_name
            )

        except Exception:
            logger.exception("Failed to initialize MongoDBService")
            raise

    def test_connection(self):
        logger.info("Testing MongoDB connection")

        try:
            result = self.client.admin.command("ping")

            logger.info("MongoDB connection successful")

            return result

        except Exception:
            logger.exception("MongoDB connection failed")
            raise

    def get_collection(self, collection_name):
        logger.info(
            "Getting MongoDB collection | collection=%s",
            collection_name
        )

        try:
            collection = self.db[collection_name]

            logger.info(
                "MongoDB collection ready | collection=%s",
                collection_name
            )

            return collection

        except Exception:
            logger.exception(
                "Failed to get MongoDB collection | collection=%s",
                collection_name
            )
            raise