from fastapi import FastAPI
from app.routers import chat
from app.core.handler_errors import custom_exception_handler
from app.providers.exceptions import (
    DatabaseOperationError, 
    EntityCreationError, 
    EntityNotFoundError, 
    EntityFetchError
)
from app.services.exceptions import (
    ChatServiceError, 
    ConversationError, 
    MessageError
)
from app.llm.exceptions import (
    LLMServiceError, 
    GeminiServiceError
)

app = FastAPI(title="Kopilot")

app.add_exception_handler(DatabaseOperationError, custom_exception_handler)
app.add_exception_handler(EntityCreationError, custom_exception_handler)
app.add_exception_handler(EntityNotFoundError, custom_exception_handler)
app.add_exception_handler(EntityFetchError, custom_exception_handler)

app.add_exception_handler(ChatServiceError, custom_exception_handler)
app.add_exception_handler(ConversationError, custom_exception_handler)
app.add_exception_handler(MessageError, custom_exception_handler)

app.add_exception_handler(LLMServiceError, custom_exception_handler)
app.add_exception_handler(GeminiServiceError, custom_exception_handler)

versionAPI = "v1"
app.include_router(chat.router, prefix=f"/api/{versionAPI}/chat")