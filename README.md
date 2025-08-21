## 📜 Table of Contents
- [📜 Table of Contents](#-table-of-contents)
- [🌎 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🛠️ Technology Stack](#️-technology-stack)
- [📋 Prerequisites](#-prerequisites)
- [🚀 Getting Started](#-getting-started)
- [▶️ Makefile Commands](#️-makefile-commands)
- [📝 API Usage](#-api-usage)
  - [Starting a Conversation](#starting-a-conversation)
  - [Continuing a Conversation](#continuing-a-conversation)
  - [Response Format](#response-format)
- [Evidence](#evidence)
  - [📝 TODO](#-todo)

---

## 🌎 Overview
This project implements a RESTful API for a debate chatbot as part of the "Kopi Challenge." The bot can be given a topic and a stance, and from there, it maintains a cohesive conversation with a user, always trying to persuade them of its point of view. Conversation persistence is handled via a `conversation_id`.

## ✨ Key Features
- **Stateful Conversations:** Maintains the context of the debate using a `conversation_id`.
- **Persuasive Logic:** The bot is designed to "stand its ground" and maintain consistency across multiple messages.
- **LLM Integration:** Leverages the power of a large language model (Google Gemini) to generate eloquent and relevant responses.
- **Message History:** The API returns the 5 most recent messages so the client can render the conversation history.
- **Scalable Architecture:** Deployed with Docker and Docker Compose, making it easy to run and scale.

## 🛠️ Technology Stack
- **Language:** Python
- **API Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Database:** MySQL (for storing conversation history)
- **Language Model (LLM):** Google Gemini
- **Containerization:** Docker, Docker Compose

## 📋 Prerequisites
Ensure you have the following tools installed on your local system:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## 🚀 Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [YOUR-REPOSITORY-URL]
    cd [DIRECTORY-NAME]
    ```

2.  **Set up environment variables:**
    Create a `.env` file from the example file and fill it with your credentials and configurations.
    ```bash
    cp .env.example .env
    ```
    Make sure to fill in all the variables in the `.env` file (see the [Environment Variables](#️-environment-variables) section).

3.  **Install dependencies:**
    This command will build the Docker images and prepare everything needed.
    ```bash
    make install
    ```

4.  **Run the application:**
    This command will start the API and the database.
    ```bash
    make run
    ```
    - The API will be available at `http://localhost:8000`.
    - The interactive documentation (Swagger UI) will be at `http://localhost:8000/docs`.

## ▶️ Makefile Commands
This project includes a `Makefile` to simplify common development tasks.

- Usage:
  - `make`: Shows a list of all available commands.

- Dependencies
  - `make install` : Install all requirements to run the service.

- Testing
  - `make test` : Runs the automated test suite.

- Service Management
  - `make run` : Starts all services (API and database) in detached mode.
  - `make down` : Stops and removes the containers of the running services.
  - `make clean` : Stops the services, and removes associated containers and volumes.

## 📝 API Usage

The API has a single main endpoint to manage the conversation.

> API Docs: http://localhost:8000/docs

### Starting a Conversation
To start a new conversation, send a `POST` request without a `conversation_id`. The first message must define the topic and the bot's stance.

> Endpoint:  `http://localhost:8000/api/v1/chat/conversation`

**Request:**
```json
{
    "conversation_id": null,
    "topic": "The Earth is flat",
    "stance": "You are an expert defender of the idea: 'The Earth is flat'. Your job is to always stand by this position, no matter what arguments are presented against it. Never admit anything that contradicts 'The Earth is flat'. Answer persuasively, using examples, logic, and simple explanations. Always reinforce that The Earth is flat.Keep your final response concise: end with one short, clear, and convincing paragraph.",
    "message": "I want to debate whether the Earth is flat. You must argue that it is."
}
```

### Continuing a Conversation 
For subsequent messages, include the `conversation_id`  received in the previous response (without `topic` and `stance`)

> Endpoint:  `http://localhost:8000/api/v1/chat/conversation`

**Request:**
```json
{
    "conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "message": "But science has proven it's round with photos from space."
}
```

### Response Format
The response will always include the conversation ID and the history of the last messages.

**Response**:
```json
{
    "conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "message": [
        {
            "role": "user",
            "message": "I want to debate whether the Earth is flat. You must argue that it is."
        },
        {
            "role": "bot",
            "message": "Of course. It's a common misconception that it is a sphere. The so-called 'photos' are manipulations. Our sensory evidence tells us the ground beneath our feet is flat."
        },
        {
            "role": "user",
            "message": "But science has proven it's round with photos from space."
        },
        {
            "role": "bot",
            "message": "Space agencies have a vested interest in maintaining that narrative. If you consider the physics of water, it always finds its level. On a giant sphere, we would see a curvature in the oceans, but we don't."
        }
    ]
}
```

## Evidence

![](https://github.com/fereicod/chat_bot/blob/main/evidence/init_conversation_local.png) ![](https://github.com/fereicod/chat_bot/blob/main/evidence/continue_conversation_local.png)
![](https://github.com/fereicod/chat_bot/blob/main/evidence/init_conversation_dev.png) ![](https://github.com/fereicod/chat_bot/blob/main/evidence/continue_conversation_dev.png)

### 📝 TODO

- Add testing
- API security (Token, Auth, ...)