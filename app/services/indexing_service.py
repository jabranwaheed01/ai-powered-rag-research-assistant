
# import os

# from app.services.sycamore_processor import SycamoreProcessor
# from app.services.embedding_service import EmbeddingService
# from app.services.retriever_service import RetrieverService


# class IndexingService:

#     def __init__(self):
#         self.processor = SycamoreProcessor()
#         self.embedding_service = EmbeddingService()
#         self.retriever = RetrieverService()

#     def index_pdf(self, pdf_path: str):

#         chunks = self.processor.process_pdf(pdf_path)

#         texts = []
#         valid_chunks = []

#         for chunk in chunks:

#             text = getattr(
#                 chunk,
#                 "text_representation",
#                 None
#             )

#             if not text:
#                 text = getattr(
#                     chunk,
#                     "text",
#                     None
#                 )

#             if not text:
#                 continue

#             text = str(text).strip()

#             if not text:
#                 continue

#             texts.append(text)
#             valid_chunks.append(chunk)

#         if not texts:
#             print(
#                 f"No valid chunks found for "
#                 f"{os.path.basename(pdf_path)}"
#             )
#             return

#         print(
#             f"Generating embeddings for "
#             f"{len(texts)} chunks..."
#         )

#         embeddings = self.embedding_service.generate_embeddings(
#             texts
#         )

#         vectors = []

#         for i, (chunk, text, embedding) in enumerate(
#             zip(valid_chunks, texts, embeddings)
#         ):

#             metadata = {
#                 "text": text,
#                 "source": pdf_path,
#                 "document_name": os.path.basename(pdf_path),
#                 "topic": os.path.basename(
#                     os.path.dirname(pdf_path)
#                 ).lower(),
#                 "year": chunk.properties.get(
#                     "year",
#                     2023
#                 )
#             }

#             vector = self.retriever.create_vector(
#                 vector_id=(
#                     f"{os.path.basename(pdf_path)}-{i}"
#                 ),
#                 embedding=embedding,
#                 metadata=metadata
#             )

#             vectors.append(vector)

#         if vectors:
#             self.retriever.upsert_vectors(vectors)

#         print(
#             f"Indexed {os.path.basename(pdf_path)}: "
#             f"{len(vectors)} chunks"
#         )

#     def index_all(self, data_dir="data/raw"):

#         for topic in sorted(os.listdir(data_dir)):

#             topic_path = os.path.join(data_dir, topic)

#             if not os.path.isdir(topic_path):
#                 continue

#             for filename in sorted(os.listdir(topic_path)):

#                 if filename.lower().endswith(".pdf"):

#                     pdf_path = os.path.join(topic_path, filename)

#                     print(f"\nProcessing PDF: {pdf_path}")

#                     self.index_pdf(pdf_path)



# if __name__ == "__main__":
#     service = IndexingService()
#     service.index_all()



import logging
import os

from app.services.sycamore_processor import SycamoreProcessor
from app.services.embedding_service import EmbeddingService
from app.services.retriever_service import RetrieverService


logger = logging.getLogger(__name__)


class IndexingService:

    def __init__(self):

        logger.info("Initializing IndexingService")

        self.processor = SycamoreProcessor()
        self.embedding_service = EmbeddingService()
        self.retriever = RetrieverService()

        logger.info(
            "IndexingService initialized successfully"
        )

    def index_pdf(self, pdf_path: str):

        document_name = os.path.basename(pdf_path)

        logger.info(
            "Starting PDF indexing | document=%s",
            document_name
        )

        try:

            chunks = self.processor.process_pdf(
                pdf_path
            )

            logger.info(
                "PDF processed | document=%s | chunks=%d",
                document_name,
                len(chunks)
            )

            texts = []
            valid_chunks = []

            for chunk in chunks:

                text = getattr(
                    chunk,
                    "text_representation",
                    None
                )

                if not text:
                    text = getattr(
                        chunk,
                        "text",
                        None
                    )

                if not text:
                    continue

                text = str(text).strip()

                if not text:
                    continue

                texts.append(text)
                valid_chunks.append(chunk)

            if not texts:

                logger.warning(
                    "No valid chunks found | document=%s",
                    document_name
                )

                return

            logger.info(
                "Valid chunks identified | document=%s | count=%d",
                document_name,
                len(texts)
            )

            embeddings = self.embedding_service.generate_embeddings(
                texts
            )

            logger.info(
                "Embeddings generated | document=%s | count=%d",
                document_name,
                len(embeddings)
            )

            vectors = []

            for i, (chunk, text, embedding) in enumerate(
                zip(
                    valid_chunks,
                    texts,
                    embeddings
                )
            ):

                metadata = {
                    "text": text,
                    "source": pdf_path,
                    "document_name": document_name,
                    "topic": os.path.basename(
                        os.path.dirname(pdf_path)
                    ).lower(),
                    "year": chunk.properties.get(
                        "year",
                        2023
                    )
                }

                vector = self.retriever.create_vector(
                    vector_id=f"{document_name}-{i}",
                    embedding=embedding,
                    metadata=metadata
                )

                vectors.append(vector)

            logger.info(
                "Vectors created | document=%s | count=%d",
                document_name,
                len(vectors)
            )

            if vectors:

                self.retriever.upsert_vectors(
                    vectors
                )

            logger.info(
                "PDF indexing completed | document=%s | vectors=%d",
                document_name,
                len(vectors)
            )

        except Exception:

            logger.exception(
                "Failed to index PDF | document=%s",
                document_name
            )

            raise

    def index_all(self, data_dir="data/raw"):

        logger.info(
            "Starting indexing of all PDFs | directory=%s",
            data_dir
        )

        try:

            for topic in sorted(
                os.listdir(data_dir)
            ):

                topic_path = os.path.join(
                    data_dir,
                    topic
                )

                if not os.path.isdir(topic_path):
                    continue

                for filename in sorted(
                    os.listdir(topic_path)
                ):

                    if filename.lower().endswith(".pdf"):

                        pdf_path = os.path.join(
                            topic_path,
                            filename
                        )

                        logger.info(
                            "Processing PDF | path=%s",
                            pdf_path
                        )

                        self.index_pdf(
                            pdf_path
                        )

            logger.info(
                "All PDF indexing completed"
            )

        except Exception:

            logger.exception(
                "Failed during full PDF indexing"
            )

            raise


if __name__ == "__main__":

    service = IndexingService()

    service.index_all()