

import logging

from app.services.retriever_service import RetrieverService
from app.services.generator_service import GeneratorService
from app.utils.citation import format_citations
from app.services.chat_manager import ChatManager


logger = logging.getLogger(__name__)


class ChatbotService:

    def __init__(self):
        self.retriever = RetrieverService()
        self.generator = GeneratorService()
        self.chat_manager = ChatManager()

    def ask(
        self,
        query: str,
        top_k: int = 5,
        topic: str = None,
        year: int = None,
        mode: str = "qa",
        session_id: str = None
    ):

        logger.info(
            "Processing query | mode=%s | topic=%s | year=%s",
            mode,
            topic,
            year
        )

        results = self.retriever.search(
            query=query,
            top_k=top_k,
            topic=topic,
            year=year
        )

        matches = results.get("matches", [])

        logger.info(
            "Retrieved %d documents for query",
            len(matches)
        )

        context_parts = []

        for match in matches:

            text = match["metadata"].get("text", "")
            document_name = match["metadata"].get(
                "document_name",
                "Unknown Document"
            )

            context_parts.append(
                f"{text}\n[{document_name}]"
            )

        context = "\n\n".join(context_parts)

        logger.info(
            "Context prepared | characters=%d",
            len(context)
        )

        if mode == "summary":

            logger.info("Generating summary")

            answer = self.generator.generate_summary(
                query=query,
                context=context
            )

        else:

            logger.info("Generating answer")

            answer = self.generator.generate_answer(
                query=query,
                context=context
            )

        citations = format_citations(
            matches
        )

        logger.info(
            "Generated response | citations=%d",
            len(citations)
        )

        if session_id:

            self.chat_manager.add_message(
                session_id=session_id,
                query=query,
                answer=answer,
                sources=citations
            )

            logger.info(
                "Chat message saved | session_id=%s",
                session_id
            )

        return {
            "answer": answer,
            "sources": citations
        }

    def ask_stream(
        self,
        query: str,
        top_k: int = 5,
        topic: str = None,
        year: int = None,
        mode: str = "qa",
        session_id: str = None
    ):

        logger.info(
            "Processing streaming query | mode=%s | topic=%s | year=%s",
            mode,
            topic,
            year
        )

        results = self.retriever.search(
            query=query,
            top_k=top_k,
            topic=topic,
            year=year
        )

        matches = results.get("matches", [])

        logger.info(
            "Retrieved %d documents for streaming query",
            len(matches)
        )

        context_parts = []

        for match in matches:

            text = match["metadata"].get("text", "")
            document_name = match["metadata"].get(
                "document_name",
                "Unknown Document"
            )

            context_parts.append(
                f"{text}\n[{document_name}]"
            )

        context = "\n\n".join(context_parts)

        logger.info(
            "Streaming context prepared | characters=%d",
            len(context)
        )

        citations = format_citations(matches)

        answer = ""

        if mode == "summary":

            logger.info("Generating streaming summary")

            answer = self.generator.generate_summary(
                query=query,
                context=context
            )

            yield answer

        else:

            logger.info("Starting answer stream")

            for chunk in self.generator.generate_answer_stream(
                query=query,
                context=context
            ):

                answer += chunk

                yield chunk

            logger.info(
                "Answer streaming completed | citations=%d",
                len(citations)
            )

        if session_id:

            self.chat_manager.add_message(
                session_id=session_id,
                query=query,
                answer=answer,
                sources=citations
            )

            logger.info(
                "Streaming chat saved | session_id=%s",
                session_id
            )    