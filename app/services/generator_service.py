
import logging

from groq import Groq

from app.core.config import settings


logger = logging.getLogger(__name__)


class GeneratorService:

    def __init__(self):

        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing in .env")

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL

        logger.info(
            "GeneratorService initialized | model=%s",
            self.model
        )

    def generate_answer(self, query: str, context: str):

        context = context[:10000]

        logger.info(
            "Generating answer | context_length=%d",
            len(context)
        )

        prompt = f"""
You are a research assistant.

Answer the question using only the provided context.

Rules:
- Do not use tables.
- Do not use HTML tags.
- Use short paragraphs or simple bullet points.
- Keep the answer concise.
- Answer in 4-6 clear bullet points when appropriate.
- Give a clear and direct answer.
- Use only information supported by the context.
- Do not add unsupported information.
- Do not ask for more information.
- Avoid repeating the same point.
- Keep the answer focused on the question.

Context:
{context}

Question:
{query}

Answer:
"""

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=700
            )

            answer = response.choices[0].message.content

            logger.info(
                "Answer generated successfully | length=%d",
                len(answer or "")
            )

            return answer

        except Exception:
            logger.exception("Failed to generate answer")
            raise

    def generate_summary(self, query: str, context: str):

        context = context[:10000]

        logger.info(
            "Generating summary | context_length=%d",
            len(context)
        )

        prompt = f"""
You are a research assistant.

Create a structured research summary using only the provided context.

Rules:
- Do not use information outside the context.
- Do not use tables.
- Use clear headings and bullet points.
- Keep the summary focused on the question.
- Include the main findings, important points, and conclusion.
- Avoid repetition.
- Do not ask for more information.
- Add the document name in citation format like [DOCUMENT_NAME]
  after important points.

Context:
{context}

Question:
{query}

Research Summary:
"""

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=700
            )

            summary = response.choices[0].message.content

            logger.info(
                "Summary generated successfully | length=%d",
                len(summary or "")
            )

            return summary

        except Exception:
            logger.exception("Failed to generate summary")
            raise

    def generate_answer_stream(self, query: str, context: str):

        context = context[:10000]

        logger.info(
            "Starting answer stream | context_length=%d",
            len(context)
        )

        prompt = f"""
You are a research assistant.

Answer the question using only the provided context.

Rules:
- Do not use tables.
- Do not use HTML tags.
- Use short paragraphs or simple bullet points.
- Keep the answer concise.
- Use only information supported by the context.
- Do not add unsupported information.
- Keep the answer focused on the question.

Context:
{context}

Question:
{query}

Answer:
"""

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=700,
                stream=True
            )

            for chunk in response:

                content = chunk.choices[0].delta.content

                if content:
                    yield content

            logger.info("Answer stream completed successfully")

        except Exception:
            logger.exception("Failed during answer streaming")
            raise
