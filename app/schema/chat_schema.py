from typing import Optional, Literal
from pydantic import BaseModel


class Conversation(BaseModel):
    conversation_id: Optional[str] = None

class MessagenRequest(Conversation):
    message: str

class ConversationTopic(MessagenRequest):
    topic: str
    stance: str

class MessageResponse(BaseModel):
    role: Literal["user", "bot"]
    message: str

class ConversationResponse(BaseModel):
    conversation_id: str
    message: list[MessageResponse]

