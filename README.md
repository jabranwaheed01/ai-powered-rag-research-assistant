# AI-Powered RAG Research Assistant

An AI-powered research assistant that uses Retrieval-Augmented Generation (RAG) to answer questions from research documents with relevant source citations.

## Overview

The system processes PDF research documents, converts their content into embeddings, stores them in Pinecone, retrieves relevant information based on the user's query, and uses a Groq LLM to generate a grounded answer.

The application also supports topic/year filters and MongoDB-based chat session history.

## RAG Workflow

```text
PDF Documents
      ↓
Sycamore PDF Processing
      ↓
Text Chunks
      ↓
BGE-M3 Embeddings
      ↓
Pinecone Vector Database
      ↓
Semantic Search
      ↓
Relevant Chunks
      ↓
Groq LLM
      ↓
Answer + Citations
      ↓
FastAPI API
      ↓
Gradio UI / Future Flutter UI
```

## Features

* PDF document processing
* Text chunking using Sycamore
* BGE-M3 embeddings
* Pinecone vector search
* Semantic retrieval
* Topic and year filtering
* Groq LLM answer generation
* Streaming responses
* Source citations
* MongoDB chat sessions
* FastAPI REST API
* Gradio frontend
* Centralized environment configuration
* Application logging
* Global exception handling
* Pydantic request/response validation

## Tech Stack

* **Python 3.13**
* **FastAPI**
* **Uvicorn**
* **Sycamore AI**
* **Ollama**
* **BGE-M3**
* **Pinecone**
* **Groq**
* **MongoDB**
* **Gradio**
* **Pydantic**

## Project Structure

```text
AI-Powered RAG Research Assistant/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── chat_routes.py
│   │       ├── chat_session_routes.py
│   │       ├── embedding_routes.py
│   │       └── health.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logging.py
│   │   ├── exceptions.py
│   │   └── exception_handlers.py
│   │
│   ├── models/
│   │   └── chat_model.py
│   │
│   ├── services/
│   │   ├── chatbot_service.py
│   │   ├── chat_manager.py
│   │   ├── embedding_service.py
│   │   ├── generator_service.py
│   │   ├── indexing_service.py
│   │   ├── mongodb_service.py
│   │   ├── retriever_service.py
│   │   └── sycamore_processor.py
│   │
│   └── utils/
│       └── citation.py
│
├── data/
│   └── raw/
│
├── tests/
│
├── ui/
│   └── gradio_app.py
│
├── .env
├── .env.example
├── .gitignore
├── index_documents.py
├── requirements.txt
├── README.md
└── run.py
```

## Installation

Clone the repository and open the project directory:

```bash
cd "AI-Powered RAG Research Assistant"
```

Create and activate the Python environment:

```bash
python3.13 -m venv .venv313
source .venv313/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
MONGODB_URI=your_mongodb_uri

MONGODB_DB=rag_research_assistant
PINECONE_INDEX_NAME=rag-research-assistant-bge
EMBEDDING_MODEL=bge-m3
GROQ_MODEL=openai/gpt-oss-20b
```

Do not commit the `.env` file because it contains secret API credentials.

## Ollama Setup

Install Ollama and make sure it is running.

Pull the BGE-M3 embedding model:

```bash
ollama pull bge-m3
```

Verify the model:

```bash
ollama list
```

## Pinecone Configuration

The application uses the following Pinecone index configuration:

```text
Index Name: rag-research-assistant-bge
Dimension: 1024
Metric: cosine
Cloud: AWS
Region: us-east-1
```

## Document Indexing

Place research PDFs inside:

```text
data/raw/
```

Example:

```text
data/raw/environment/climate-change.pdf
data/raw/health/heath-care.pdf
data/raw/economy/Economy.pdf
```

Run the indexing process:

```bash
python index_documents.py
```

The indexing pipeline processes the PDFs, generates BGE-M3 embeddings, and stores vectors and metadata in Pinecone.

## Running the Backend

Start the FastAPI server:

```bash
uvicorn run:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health Check

```text
GET /api/v1/health
```

### Ask Question

```text
POST /api/v1/ask
```

### Streaming Question

```text
POST /api/v1/ask/stream
```

### Create Embedding

```text
POST /api/v1/embed
```

### Create Chat Session

```text
POST /api/v1/chat/sessions
```

### Get Chat Session

```text
GET /api/v1/chat/sessions/{session_id}
```

### Delete Chat Session

```text
DELETE /api/v1/chat/sessions/{session_id}
```

## Example Request

```json
{
  "query": "What are the main causes of climate change?",
  "top_k": 5,
  "topic": "environment",
  "year": 2023,
  "mode": "qa"
}
```

The API retrieves relevant document chunks and generates an answer using the retrieved context.

## Topic and Year Filters

The retrieval system supports metadata filtering.

Example:

```json
{
  "query": "What are the effects of climate change?",
  "top_k": 5,
  "topic": "environment",
  "year": 2023,
  "mode": "qa"
}
```

This limits retrieval to documents matching the selected topic and year.

## Chat Sessions

MongoDB stores conversation history using a session ID.

The flow is:

```text
Create Session
      ↓
Ask Question with session_id
      ↓
Generate Answer
      ↓
Save Query + Answer + Sources
      ↓
Retrieve Chat History
```

## Gradio UI

Start the Gradio frontend with:

```bash
python -m ui.gradio_app
```

The UI provides:

* Chat interface
* Topic filter
* Year filter
* Question input
* Streaming responses
* Sources
* Clear chat
* New chat
* Clear filters

## Error Handling and Logging

The application includes centralized logging and global exception handling.

Application errors are handled through custom exceptions and returned as structured JSON responses.

Example:

```json
{
  "success": false,
  "error": "Internal server error"
}
```

## Testing

Run the test suite using:

```bash
pytest
```

## Project Goal

The goal of this project is to provide a reliable research assistant that answers questions using information retrieved from trusted research documents instead of relying only on the language model's internal knowledge.

## Future Improvements

* Flutter frontend integration
* Improved citation handling for streaming responses
* More document formats
* Advanced retrieval and reranking
* Authentication and user management
* Production deployment
