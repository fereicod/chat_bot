from typing import Literal, Optional
from app.providers.chat_provider import ConversationProvider, MessageProvider
from app.database.models import Conversation, Message
from app.schema.api_chat import ConversationRequest, MessageResponse
from fastapi import HTTPException
import uuid


ROLE_MAP: dict[str, Literal["user", "bot"]] = {
    "user": "user",
    "model": "bot"
}

class ChatService:
    def __init__(self, conversation_provider: ConversationProvider, message_provider: MessageProvider):
        self.conversation_provider = conversation_provider
        self.message_provider = message_provider 

    def get_conversation_by_id(self, conversation_id: str) -> Conversation:
        conversation = self.conversation_provider.get_by_id(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation

    def create_conversation(self, conversation_request: ConversationRequest) -> str:
        if conversation_request.conversation_id:
            existing_conversation = self.get_conversation_by_id(conversation_request.conversation_id)
            if existing_conversation:
                raise HTTPException(status_code=400, detail="Conversation already exists")
    
        conversation = Conversation(
            id=str(uuid.uuid4()),
            topic=conversation_request.topic, # type: ignore
            stance=conversation_request.stance # type: ignore
        )
        new_conversation = self.conversation_provider.create(conversation)
        if not new_conversation:
            raise HTTPException(status_code=500, detail="Failed to create conversation")
        
        return conversation.id
        
    def create_message(self, conversation_id: str, role: str, content: str) -> None:
        conversation = self.get_conversation_by_id(conversation_id)
        message = Message(
            conversation_id=conversation.id,
            message_role=role,
            content=content
        )
        message = self.message_provider.create(message)
        if not message:
            raise HTTPException(status_code=500, detail="Failed to create message")
    
    def get_messages_by_conversation_id(self, conversation_id: str, limit: int = 10) -> Optional[list[MessageResponse]]:
        conversation = self.conversation_provider.get_by_id(conversation_id)
        if not conversation:
            messages = []
        else:
            messages = self.message_provider.get_messages(conversation.id, limit)
        return [
            MessageResponse(
                role=ROLE_MAP.get(msg.message_role, "user"),
                message=msg.content
            ) for msg in messages
        ] if messages else []
