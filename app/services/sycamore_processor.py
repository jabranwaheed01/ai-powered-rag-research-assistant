
# import os
# import sycamore
# from pypdf import PdfReader
# from sycamore.data import Document, Element


# class SycamoreProcessor:

#     def __init__(self):
#         self.context = sycamore.init(
#             exec_mode=sycamore.EXEC_LOCAL
#         )

#     def process_pdf(self, pdf_path: str):

#         document_name = os.path.basename(pdf_path)

#         topic = os.path.basename(
#             os.path.dirname(pdf_path)
#         ).lower()

#         year_map = {
#             "climate-change.pdf": 2023,
#             "heath-care.pdf": 2023,
#             "Economy.pdf": 2023
#         }

#         year = year_map.get(document_name, 2023)

#         reader = PdfReader(pdf_path)

#         text_parts = []

#         for page in reader.pages:
#             page_text = page.extract_text()

#             if page_text:
#                 text_parts.append(page_text)

#         text = "\n".join(text_parts).strip()

#         if not text:
#             raise ValueError(
#                 f"No text could be extracted from: {pdf_path}"
#             )

#         chunk_size = 10000
#         overlap = 500

#         chunks = []

#         start = 0
#         chunk_number = 0

#         while start < len(text):

#             end = start + chunk_size

#             chunk_text = text[start:end].strip()

#             if chunk_text:

#                 element = Element(
#                     type="text",
#                     text_representation=chunk_text,
#                     properties={
#                         "source": pdf_path,
#                         "document_name": document_name,
#                         "topic": topic,
#                         "year": year,
#                         "chunk_number": chunk_number
#                     }
#                 )

#                 document = Document(
#                     elements=[element],
#                     properties={
#                         "source": pdf_path,
#                         "document_name": document_name,
#                         "topic": topic,
#                         "year": year,
#                         "chunk_number": chunk_number
#                     }
#                 )

#                 element.properties["text"] = chunk_text

#                 chunks.append(element)

#                 chunk_number += 1

#             start = end - overlap

#         print(
#             f"Sycamore processed {document_name}: "
#             f"{len(chunks)} chunks"
#         )

#         return chunks



import logging
import os

import sycamore
from pypdf import PdfReader
from sycamore.data import Document, Element


logger = logging.getLogger(__name__)


class SycamoreProcessor:

    def __init__(self):

        logger.info(
            "Initializing Sycamore processor"
        )

        self.context = sycamore.init(
            exec_mode=sycamore.EXEC_LOCAL
        )

        logger.info(
            "Sycamore processor initialized successfully"
        )

    def process_pdf(self, pdf_path: str):

        logger.info(
            "Starting PDF processing | path=%s",
            pdf_path
        )

        try:

            document_name = os.path.basename(pdf_path)

            topic = os.path.basename(
                os.path.dirname(pdf_path)
            ).lower()

            year_map = {
                "climate-change.pdf": 2023,
                "heath-care.pdf": 2023,
                "Economy.pdf": 2023
            }

            year = year_map.get(
                document_name,
                2023
            )

            logger.info(
                "PDF metadata identified | document=%s | topic=%s | year=%s",
                document_name,
                topic,
                year
            )

            reader = PdfReader(pdf_path)

            logger.info(
                "PDF loaded successfully | document=%s | pages=%d",
                document_name,
                len(reader.pages)
            )

            text_parts = []

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text_parts.append(page_text)

            text = "\n".join(text_parts).strip()

            logger.info(
                "Text extraction completed | document=%s | characters=%d",
                document_name,
                len(text)
            )

            if not text:

                raise ValueError(
                    f"No text could be extracted from: {pdf_path}"
                )

            chunk_size = 10000
            overlap = 500

            chunks = []

            start = 0
            chunk_number = 0

            while start < len(text):

                end = start + chunk_size

                chunk_text = text[start:end].strip()

                if chunk_text:

                    element = Element(
                        type="text",
                        text_representation=chunk_text,
                        properties={
                            "source": pdf_path,
                            "document_name": document_name,
                            "topic": topic,
                            "year": year,
                            "chunk_number": chunk_number
                        }
                    )

                    document = Document(
                        elements=[element],
                        properties={
                            "source": pdf_path,
                            "document_name": document_name,
                            "topic": topic,
                            "year": year,
                            "chunk_number": chunk_number
                        }
                    )

                    element.properties["text"] = chunk_text

                    chunks.append(element)

                    chunk_number += 1

                start = end - overlap

            logger.info(
                "PDF processing completed | document=%s | chunks=%d",
                document_name,
                len(chunks)
            )

            return chunks

        except Exception:

            logger.exception(
                "Failed to process PDF | path=%s",
                pdf_path
            )

            raise