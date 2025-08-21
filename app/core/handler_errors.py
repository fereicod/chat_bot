from fastapi import HTTPException, Request
from app.providers.exceptions import DatabaseOperationError, EntityCreationError, EntityNotFoundError, EntityFetchError
from app.services.exceptions import ChatServiceError, ConversationError, MessageError
from app.llm.exceptions import LLMServiceError, GeminiServiceError

async def custom_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, (ConversationError, MessageError)):
        raise HTTPException(status_code=400, detail=str(exc))
    
    elif isinstance(exc, (EntityNotFoundError, EntityFetchError)):
        raise HTTPException(status_code=404, detail="Resource not found")
    
    elif isinstance(exc, (DatabaseOperationError, ChatServiceError, EntityCreationError)):
        raise HTTPException(status_code=500, detail="Internal server error")

    elif isinstance(exc, (LLMServiceError, GeminiServiceError)):
        raise HTTPException(status_code=503, detail="AI service unavailable")
    
    else:
        raise HTTPException(status_code=500, detail="Something went wrong")