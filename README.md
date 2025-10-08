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
    git clone https://github.com/dangeamro/qtec-ai-chatbot.git
    ```
2.  **Create a virtual environment and activate it:**

    **Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
    **Linux/macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a PostgreSQL Database:**
    Ensure you have a PostgreSQL server running. Create a new database for this project (e.g., `qtec_chatbot_db`).

5.  **Create a `.env` file** and configure your database connection and `GOOGLE_API_KEY`:
    Create a file named `.env` in the project root with the following content, replacing placeholders with your actual database credentials and API key:
    ```
    DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
    GOOGLE_API_KEY=<your-api-key>
    ```
    Example `DATABASE_URL` for a local PostgreSQL setup: `postgres://myuser:mypassword@localhost:5432/qtec_chatbot_db`

6.  **Run the database migrations:**
    ```bash
    python manage.py migrate
    ```
7.  **Create an Admin User (Superuser):**
    Run the following command to create an administrator account for the Django admin panel. Follow the prompts to set up your username, email, and password.
    ```bash
    python manage.py createsuperuser
    ```
    You can access the Django admin panel at `http://127.0.0.1:8000/admin/` after starting the development server.

8.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## API Usage

### Chat with the AI

Access the chat interface by navigating to `http://127.0.0.1:8000/` in your web browser after starting the development server. Type your message in the input field and press "Send" or Enter to interact with the chatbot.

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