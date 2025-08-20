from fastapi import Depends
from sqlmodel import Session
from app.database.manager import get_session
from app.services.services_handler import ChatServiceHandler
from app.services.chat_services import ChatService
from app.llm.google_gemini import GeminiServices
from app.schema.api_chat import ConversationRequest


def get_chat_services(session: Session = Depends(get_session)) -> ChatService:
    handler = ChatServiceHandler(session)
    return handler.get_services()

def get_gemini_service(
    chat_service: ChatService = Depends(get_chat_services),
):
    def _factory(conversation: ConversationRequest) -> GeminiServices:
        return GeminiServices(
            service=chat_service,
            conversation=conversation,
        )
    return _factory
