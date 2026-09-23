
# import ollama


# class EmbeddingService:

#     def __init__(self, model_name: str = "bge-m3"):
#         self.model_name = model_name

#     def generate_embedding(self, text: str) -> list[float]:

#         response = ollama.embed(
#             model=self.model_name,
#             input=text
#         )

#         embedding = response.embeddings[0]

#         if not embedding:
#             raise ValueError(
#                 f"Embedding is empty. Ollama model '{self.model_name}' "
#                 "did not return an embedding."
#             )

#         return embedding  

#     def generate_embeddings(
#         self,
#         texts: list[str],
#         batch_size: int = 10
#     ) -> list[list[float]]:

#         if not texts:
#             return []

#         all_embeddings = []

#         total = len(texts)

#         for start in range(0, total, batch_size):

#             batch = texts[start:start + batch_size]

#             print(
#                 f"Embedding batch "
#                 f"{start + 1}-{min(start + batch_size, total)} "
#                 f"of {total}"
#             )

#             response = ollama.embed(
#                 model=self.model_name,
#                 input=batch
#             )

#             embeddings = response.embeddings

#             if not embeddings:
#                 raise ValueError(
#                     f"Ollama model '{self.model_name}' "
#                     "did not return embeddings."
#                 )

#             all_embeddings.extend(embeddings)

#         return all_embeddings    





import logging

import ollama


logger = logging.getLogger(__name__)


class EmbeddingService:

    def __init__(self, model_name: str = "bge-m3"):

        self.model_name = model_name

        logger.info(
            "EmbeddingService initialized | model=%s",
            self.model_name
        )

    def generate_embedding(
        self,
        text: str
    ) -> list[float]:

        logger.info(
            "Generating embedding | text_length=%d",
            len(text)
        )

        try:

            response = ollama.embed(
                model=self.model_name,
                input=text
            )

            embedding = response.embeddings[0]

            if not embedding:
                raise ValueError(
                    f"Embedding is empty. Ollama model "
                    f"'{self.model_name}' did not return an embedding."
                )

            logger.info(
                "Embedding generated successfully | dimensions=%d",
                len(embedding)
            )

            return embedding

        except Exception:
            logger.exception(
                "Failed to generate embedding | model=%s",
                self.model_name
            )
            raise

    def generate_embeddings(
        self,
        texts: list[str],
        batch_size: int = 10
    ) -> list[list[float]]:

        if not texts:

            logger.warning(
                "No texts provided for embedding"
            )

            return []

        all_embeddings = []

        total = len(texts)

        logger.info(
            "Starting batch embedding | total=%d | batch_size=%d",
            total,
            batch_size
        )

        try:

            for start in range(0, total, batch_size):

                batch = texts[start:start + batch_size]

                logger.info(
                    "Embedding batch | %d-%d of %d",
                    start + 1,
                    min(start + batch_size, total),
                    total
                )

                response = ollama.embed(
                    model=self.model_name,
                    input=batch
                )

                embeddings = response.embeddings

                if not embeddings:
                    raise ValueError(
                        f"Ollama model '{self.model_name}' "
                        "did not return embeddings."
                    )

                all_embeddings.extend(embeddings)

            logger.info(
                "Batch embedding completed | embeddings=%d",
                len(all_embeddings)
            )

            return all_embeddings

        except Exception:
            logger.exception(
                "Failed during batch embedding | model=%s",
                self.model_name
            )
            raise