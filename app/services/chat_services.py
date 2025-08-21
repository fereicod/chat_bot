from typing import Literal
from app.providers.chat_provider import ConversationProvider, MessageProvider
from app.database.models import Conversation, Message
from app.schema.api_chat import ConversationRequest, MessageResponse
from app.services.exceptions import ConversationError, MessageError
from app.services.decorators import handle_service_errors
import uuid

ROLE_MAP: dict[str, Literal["user", "bot"]] = {
    "user": "user",
    "model": "bot"
}

class ChatService:
    def __init__(self, conversation_provider: ConversationProvider, message_provider: MessageProvider):
        self.conversation_provider = conversation_provider
        self.message_provider = message_provider 

    @handle_service_errors(error_to_raise=ConversationError)
    def get_conversation_by_id(self, conversation_id: str) -> Conversation:
        conversation = self.conversation_provider.get_by_id(conversation_id)
        if not conversation:
            raise ConversationError(f"Conversation with id {conversation_id} not found")

        return conversation

    @handle_service_errors(error_to_raise=ConversationError)
    def create_conversation(self, conversation_request: ConversationRequest) -> str:
        if not conversation_request.topic or len(conversation_request.topic.strip()) < 5:
            raise ConversationError("Topic must have at least 5 characters")

        if not conversation_request.stance or len(conversation_request.stance.strip()) < 20:
            raise ConversationError("Stance must have at least 20 characters")

        if conversation_request.conversation_id:
            try:
                existing_conversation = self.conversation_provider.get_by_id(conversation_request.conversation_id)
                if existing_conversation:
                    raise ConversationError("Conversation already exists")
            except Exception:
                pass
    
        conversation = Conversation(
            id=str(uuid.uuid4()),
            topic=conversation_request.topic.strip(),
            stance=conversation_request.stance.strip()
        )
        
        new_conversation = self.conversation_provider.create(conversation)
        if not new_conversation:
            raise ConversationError("Failed to create conversation in database")
        
        return conversation.id
            
    @handle_service_errors(error_to_raise=MessageError)
    def create_message(self, conversation_id: str, role: str, content: str) -> None:
        if not content or not content.strip():
            raise MessageError("Message content cannot be empty")
        
        if role not in ["user", "model"]:
            raise MessageError(f"Invalid role '{role}'. Must be 'user' or 'model'")
        
        conversation = self.get_conversation_by_id(conversation_id)
        
        message = Message(
            conversation_id=conversation.id,
            message_role=role,
            content=content.strip()
        )
        
        created_message = self.message_provider.create(message)
        if not created_message:
            raise MessageError("Failed to create message in database")

    @handle_service_errors(error_to_raise=MessageError)
    def get_messages_by_conversation_id(self, conversation_id: str, limit: int = 10) -> list[MessageResponse]:
        if limit <= 0:
            raise MessageError("Limit must be greater than 0")
        
        if limit > 100:
            raise MessageError("Limit cannot exceed 100 messages")
        
        conversation = self.get_conversation_by_id(conversation_id)
        messages = self.message_provider.get_messages(conversation.id, limit)
        
        try:
            return [
                MessageResponse(
                    role=ROLE_MAP.get(msg.message_role, "user"),
                    message=msg.content
                ) for msg in messages
            ] if messages else []
        except Exception as e:
            raise MessageError(f"Failed to transform messages to response format: {str(e)}")
