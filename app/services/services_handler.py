from app.services.base import BaseServiceHandler
from app.providers.chat_provider import ConversationProvider, MessageProvider
from app.services.chat_services import ChatService


class ChatServiceHandler(BaseServiceHandler):

    def _setup_repositories(self) -> None:
        self.conversation_provider = ConversationProvider(self.session)
        self.message_provider = MessageProvider(self.session)
    
    def _setup_services(self) -> None:
        self.caht_service = ChatService(self.conversation_provider, self.message_provider)
    
    def get_services(self) -> ChatService:
        return self.caht_service