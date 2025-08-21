from google import genai
from google.genai import types
from app.llm.decorators import handle_gemini_errors
from app.llm.exceptions import GeminiServiceError
from app.services.chat_services import ChatService
from app.database.models import Conversation
from app.llm.constants import GENERATE_CONTENT_CONFIG
from app.schema.api_chat import ConversationRequest, ConversationResponse, MessageResponse
from app.core.config import settings
import copy

class GoogleGeminiService:
    def __init__(self, chat_service: ChatService, conversation_request: ConversationRequest):
        self.chat_service = chat_service
        self.conversation_request = conversation_request
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL

    @handle_gemini_errors(error_to_raise=GeminiServiceError, message="Failed to generate response")
    def generate_response(self, message: str) -> ConversationResponse:
        if not message or not message.strip():
            raise GeminiServiceError("User message cannot be empty")

        conversation = self._get_or_create_conversation(self.conversation_request)

        conversation_history = self.chat_service.get_messages_by_conversation_id(conversation.id, limit=10)
        
        self.chat_service.create_message(conversation.id, "user", message.strip())
        
        chat_session = self._create_chat_session(conversation_history, conversation.stance)
        response = chat_session.send_message(message.strip())
        
        if not response or not response.text or not response.text.strip():
            raise GeminiServiceError("Gemini API returned empty response")
        
        bot_response = response.text.strip()
        self.chat_service.create_message(conversation.id, "model", bot_response)

        return ConversationResponse(
            conversation_id=conversation.id,
            message=self.chat_service.get_messages_by_conversation_id(conversation.id, limit=10)
        )

    @handle_gemini_errors(error_to_raise=GeminiServiceError, message="Failed to get or create conversation")
    def _get_or_create_conversation(self, conversation_request: ConversationRequest) -> Conversation:
        if conversation_request.conversation_id:
            try:
                conversation = self.chat_service.get_conversation_by_id(conversation_request.conversation_id)
                return conversation
            except Exception:
                pass

        if not conversation_request.topic or not conversation_request.topic.strip():
            raise GeminiServiceError("Topic is required in ConversationRequest")
        
        if not conversation_request.stance or not conversation_request.stance.strip():
            raise GeminiServiceError("Stance is required in ConversationRequest")
        
        conversation = self.chat_service.create_conversation(conversation_request)
        return conversation

    @handle_gemini_errors(error_to_raise=GeminiServiceError, message="Failed to create chat session")
    def _create_chat_session(self, messages: list[MessageResponse], stance: str):
        if not isinstance(messages, list):
            raise GeminiServiceError("Invalid message history format")
        
        if not stance or not stance.strip():
            raise GeminiServiceError("Stance is required for chat session")

        try:
            history = self._convert_history_to_gemini_format(messages)

            config = copy.deepcopy(GENERATE_CONTENT_CONFIG)
            if isinstance(config.system_instruction, list):
                config.system_instruction.append(types.Part.from_text(text=stance))
            else:
                raise GeminiServiceError("config.system_instruction must be a list to append items")
            print(f"Config: {config}")
            chat_session = self.client.chats.create(
                model=self.model,
                config=config,
                history=list(history),
            )
            return chat_session
            
        except Exception as e:
            raise Exception(f"Failed to create chat session with history: {str(e)}")

    def _convert_history_to_gemini_format(self, messages: list[MessageResponse]) -> list[types.Content]:
        history = []
        print(f"History: {messages}")
        for msg in messages:
            if not hasattr(msg, 'role') or not hasattr(msg, 'message'):
                raise GeminiServiceError("Invalid message format in history")
            
            message = (
                types.UserContent(parts=[types.Part.from_text(text=msg.message)])
                if msg.role == "user"
                else types.Content(role=msg.role, parts=[types.Part.from_text(text=msg.message)])
            )
            history.append(message)
        print(f"Converted History: {history}")
        return history
