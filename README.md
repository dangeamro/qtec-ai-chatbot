# Document-Aware AI Chatbot

This project is a document-aware AI chatbot with memory, document retrieval, and real-time streaming. It's built with Django, PostgreSQL, and LangGraph.

## Project Overview

The chatbot allows users to upload `.txt` documents, which are then used as a knowledge base for the AI. The AI can answer questions about the documents, and it remembers the context of the conversation. The response from the AI is streamed in real-time.

## Features

-   **Document Upload:** Upload `.txt` files to be used as a knowledge base.
-   **Chat with Memory:** The chatbot remembers the context of the conversation.
-   **Document Retrieval:** The chatbot can retrieve relevant information from the uploaded documents to answer questions.
-   **Real-time Streaming:** The AI's response is streamed in real-time.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file** and add your `GOOGLE_API_KEY`:
    ```
    GOOGLE_API_KEY=<your-api-key>
    ```
5.  **Run the database migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## API Usage

### Upload a document

-   **Endpoint:** `POST /api/document/`
-   **Method:** `POST`
-   **Body:** `multipart/form-data` with a `file` field containing the `.txt` file.

### Send a message

-   **Endpoint:** `POST /api/chat/`
-   **Method:** `POST`
-   **Body:** `{"session_id": <session-id (optional)>, "message": "Your message here"}`

### Get chat history

-   **Endpoint:** `GET /api/session/<id>/messages/`
-   **Method:** `GET`