from fastapi import APIRouter
from app.schema.chat_schema import MessagenRequest, ConversationResponse, MessageResponse

router = APIRouter()

@router.post("/conversation", response_model=ConversationResponse)
def chat_bot(message: MessagenRequest):
    return ConversationResponse(
        conversation_id="12345",
        message=[
            MessageResponse(role="user", message=message.message),
            MessageResponse(role="bot", message="This is a response from the bot.")
        ]
    )
