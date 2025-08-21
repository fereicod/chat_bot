from sqlmodel import Session, select
from typing import Optional
from app.database.models import Conversation, Message
from app.providers.decorators import handle_db_operation
from app.providers.exceptions import EntityNotFoundError, EntityCreationError, EntityFetchError

class ConversationProvider:
    def __init__(self, session: Session):
        self.session = session
    
    @handle_db_operation(error_to_raise=EntityCreationError)
    def create(self, conversation: Conversation) -> Conversation:
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    @handle_db_operation(error_to_raise=EntityFetchError)
    def get_by_id(self, id: str) -> Optional[Conversation]:
        statement = select(Conversation).where(Conversation.id == id)
        result = self.session.exec(statement).first()
        return result


class MessageProvider:
    def __init__(self, session: Session):
        self.session = session

    @handle_db_operation(error_to_raise=EntityCreationError)
    def create(self, message: Message) -> Message:
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    @handle_db_operation(error_to_raise=EntityFetchError)
    def get_messages(self, conversation_id: str, limit: int) -> list[Message]:
        statement = select(Message).where(Message.conversation_id == conversation_id).limit(limit)
        return list(self.session.exec(statement))
