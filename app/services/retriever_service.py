
import logging

from pinecone import Pinecone, ServerlessSpec

from app.core.config import settings
from app.services.embedding_service import EmbeddingService


logger = logging.getLogger(__name__)


class RetrieverService:

    

    def __init__(self):

        if not settings.PINECONE_API_KEY:
            raise ValueError(
                "PINECONE_API_KEY is missing in .env"
            )

        self.pc = Pinecone(
            api_key=settings.PINECONE_API_KEY
        )

        self.index_name = settings.PINECONE_INDEX_NAME

        logger.info(
            "RetrieverService initialized | index=%s",
            self.index_name     #INDEX_NAME
        )

    def list_indexes(self):

        logger.info("Listing Pinecone indexes")

        try:
            return self.pc.list_indexes()

        except Exception:
            logger.exception("Failed to list Pinecone indexes")
            raise

    def create_index(self):

        logger.info(
            "Checking Pinecone index | name=%s",
            self.index_name      #INDEX_NAME
        )

        try:
            existing_indexes = self.pc.list_indexes().names()

            if self.index_name in existing_indexes:

                logger.info(
                    "Index already exists | name=%s",
                    self.index_name
                )

                return

            self.pc.create_index(
                name=self.index_name,
                dimension=1024,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

            logger.info(
                "Pinecone index created | name=%s",
                self.index_name
            )

        except Exception:
            logger.exception(
                "Failed to create Pinecone index"
            )
            raise

    def get_index(self):

        logger.info(
            "Connecting to Pinecone index | name=%s",
            self.index_name
        )

        try:

            index_info = self.pc.describe_index(
                self.index_name
            )

            return self.pc.Index(
                host=index_info.host
            )

        except Exception:
            logger.exception(
                "Failed to connect to Pinecone index"
            )
            raise

    def create_vector(
        self,
        vector_id,
        embedding,
        metadata
    ):

        return {
            "id": vector_id,
            "values": embedding,
            "metadata": metadata
        }

    def upsert_vectors(self, vectors):

        if not vectors:

            logger.warning(
                "No vectors provided for upsert"
            )

            return

        logger.info(
            "Upserting vectors | count=%d",
            len(vectors)
        )

        try:

            index = self.get_index()

            index.upsert(
                vectors=vectors
            )

            logger.info(
                "Vectors upserted successfully | count=%d",
                len(vectors)
            )

        except Exception:
            logger.exception(
                "Failed to upsert vectors"
            )
            raise

    def search(
        self,
        query: str,
        top_k: int = 5,
        topic: str = None,
        year: int = None
    ):

        logger.info(
            "Starting vector search | top_k=%d | topic=%s | year=%s",
            top_k,
            topic,
            year
        )

        try:

            embedding_service = EmbeddingService()

            query_embedding = embedding_service.generate_embedding(
                query
            )

            logger.info(
                "Query embedding generated | dimensions=%d",
                len(query_embedding)
            )

            index = self.get_index()

            query_params = {
                "vector": query_embedding,
                "top_k": top_k,
                "include_metadata": True
            }

            filter_conditions = {}

            if topic:
                filter_conditions["topic"] = {
                    "$eq": topic
                }

            if year:
                filter_conditions["year"] = {
                    "$eq": year
                }

            if filter_conditions:

                query_params["filter"] = filter_conditions

                logger.info(
                    "Applying Pinecone filters | filters=%s",
                    filter_conditions
                )

            results = index.query(
                **query_params
            )

            logger.info(
                "Vector search completed | matches=%d",
                len(results.get("matches", []))
            )

            return results

        except Exception:
            logger.exception(
                "Pinecone vector search failed"
            )
            raise
