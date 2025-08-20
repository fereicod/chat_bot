from fastapi import APIRouter, Depends
from app.services.services import get_gemini_service
from app.schema.api_chat import ConversationRequest, ConversationResponse

router = APIRouter()

@router.post("/conversation", response_model=ConversationResponse)
def chat_bot(conversation: ConversationRequest, gemini_service_factory=Depends(get_gemini_service)):
    gemini_service = gemini_service_factory(conversation)
    messages = gemini_service.send_message(conversation.message)
    return messages
