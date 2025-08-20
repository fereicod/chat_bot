from typing import Optional, Literal
from pydantic import BaseModel, model_validator


class MessagenRequest(BaseModel):
    message: str

class ConversationRequest(MessagenRequest):
    conversation_id: Optional[str] = None
    topic:  Optional[str] = None
    stance: Optional[str] = None

    @model_validator(mode="before")
    def check_topic_stance_if_no_conversation(cls, values):
        conv_id = values.get("conversation_id")
        topic = values.get("topic")
        stance = values.get("stance")

        if not conv_id:
            if not topic or not stance:
                raise ValueError("If conversation_id is empty, both topic and stance are required.")
        return values

class MessageResponse(BaseModel):
    role: Literal["user", "bot"]
    message: str

class ConversationResponse(BaseModel):
    conversation_id: str
    message: list[MessageResponse]

