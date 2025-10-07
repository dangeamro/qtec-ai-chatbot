# Research & Analysis

This document outlines the architecture, technology choices, and implementation plan for the document-aware AI chatbot.

## 1. System Architecture Overview

The system will be a monolithic Django application with a PostgreSQL database. The architecture is designed to be simple, scalable, and maintainable.

- **Backend:** Django will handle the API endpoints, business logic, and database interactions.
- **Database:** PostgreSQL will store chat sessions, messages, and documents.
- **AI Orchestration:** LangGraph will manage the flow of logic for the AI, including prompt engineering, document retrieval, and response generation.
- **LLM:** A third-party LLM API (like Groq, OpenAI, or Gemini) will be used for generating responses.

## 2. Technology Justifications

- **Django:** A robust and scalable framework for building web applications and APIs. It has a strong ecosystem and is well-suited for this project.
- **PostgreSQL:** A powerful, open-source relational database that is reliable and can handle the data requirements of this application.
- **LangGraph:** A library for building stateful, multi-actor applications with LLMs. It's ideal for orchestrating the complex logic of a chatbot with memory and document retrieval.
- **SentenceTransformers:** A library for creating state-of-the-art sentence and text embeddings, which will be used for semantic search.

## 3. Document Retrieval Plan

1.  **Upload:** Users will upload `.txt` files via a REST API endpoint.
2.  **Chunking:** The documents will be split into smaller, semantically meaningful chunks.
3.  **Embedding:** Each chunk will be converted into a vector embedding using SentenceTransformers.
4.  **Storage:** The embeddings will be stored in a way that allows for efficient similarity search (e.g., using a vector database or a simple in-memory index for this prototype).
5.  **Retrieval:** When a user sends a message, the message will be embedded, and a similarity search will be performed to find the most relevant document chunks.
6.  **Injection:** The retrieved chunks will be injected into the LLM prompt to provide context for the response.

## 4. Chat Memory Design

Chat memory will be implemented by storing the conversation history in the database.

- **`ChatSession` model:** Represents a single conversation.
- **`ChatMessage` model:** Stores each user and AI message, linked to a `ChatSession`.
- **Context:** Before generating a response, the recent chat history will be retrieved from the database and included in the prompt sent to the LLM.

## 5. Streaming Implementation

The `/api/chat/` endpoint will use Server-Sent Events (SSE) or a chunked HTTP response to stream the AI's response token-by-token. This will provide a real-time, interactive user experience.

## 6. Scalability & Extensibility

- **Scalability:** The application can be scaled by running multiple instances of the Django server and using a load balancer. The database can also be scaled independently.
- **Extensibility:** The use of LangGraph allows for the easy addition of new tools and capabilities to the AI. The system can be extended to support different document types, LLMs, and embedding models.

## 7. Testing & Validation

- **Unit Tests:** Write unit tests for the API endpoints, models, and business logic.
- **Integration Tests:** Test the integration between the different components of the system, including the database, AI orchestration, and LLM.
- **Manual Testing:** Manually test the chatbot to ensure it is functioning as expected.