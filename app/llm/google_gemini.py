from google import genai
from google.genai import types
from app.core.config import settings
from app.services.chat_services import ChatService
from app.schema.api_chat import ConversationRequest, ConversationResponse


class GeminiServices:
    def __init__(self, service: ChatService, conversation: ConversationRequest):
        self.service = service
        self.conversation = conversation

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL
        self.tools = [
            types.Tool(google_search=types.GoogleSearch()),
        ]
        self.generate_content_config: types.GenerateContentConfig
        self.system_instruction: list[types.Part] = []
        self.history: list[types.ContentOrDict] = []

        self.chat_session = None

        self._prepare_chat()

    def _add_system_instruction(self, stance: str):
        self.system_instruction.append(types.Part.from_text(text=stance))
    
    def _prepare_chat(self):
        if self.conversation.conversation_id:
            conversation_data = self.service.conversation_provider.get_by_id(self.conversation.conversation_id)
            stance = conversation_data.stance # type: ignore
        else:
            stance = self.conversation.stance
        self._add_system_instruction(stance) # type: ignore

        self.generate_content_config = types.GenerateContentConfig(
            temperature=0,
            thinking_config = types.ThinkingConfig(
                thinking_budget=-1,
            ),
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
            ],
            tools=list(self.tools),
            system_instruction=self.system_instruction,
        )
        self._create_chat_session()

    def _get_history(self):
        self.history = []
        history = self.service.get_messages_by_conversation_id(
            conversation_id=self.conversation.conversation_id, # type: ignore
        )
        print(f"History: {history}")
        if not history:
            return []
        
        for msg in history:
            if msg.role == "user":
                message = types.UserContent(
                    parts=[types.Part.from_text(text=msg.message)]
                )
            else:
                types.Content(
                    role=msg.role,
                    parts=[types.Part.from_text(text=msg.message)]
                )
            self.history.append(message)
        print(f"History after processing: {self.history}")

    def _create_chat_session(self):
        self.chat_session = self.client.chats.create(
            model=self.model,
            config=self.generate_content_config,
            history=self._get_history(),
        )

    def send_message(self, message: str) -> ConversationResponse:
        if not self.chat_session:
            raise ValueError("Chat session is not initialized.")
        
        if not self.conversation.conversation_id:
            self.conversation.conversation_id = self.service.create_conversation(
                self.conversation
            )
        
        self.service.create_message(
            conversation_id=self.conversation.conversation_id, # type: ignore
            role="user",
            content=message
        )
        
        response = self.chat_session.send_message(
            message=message,
        )
        if not response:
            raise ValueError("Failed to get a response from the chat session.")
        
        self.service.create_message(
            conversation_id=self.conversation.conversation_id, # type: ignore
            role="model",
            content=response.text # type: ignore
        )
        return ConversationResponse(
            conversation_id=self.conversation.conversation_id, # type: ignore
            message=self.service.get_messages_by_conversation_id(
                conversation_id=self.conversation.conversation_id, # type: ignore
            )
        )
