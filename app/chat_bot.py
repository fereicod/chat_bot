from google import genai
from google.genai import types
import uuid
from app.database.manager import DatabaseManager
from app.database.models import Conversation, Message
from sqlmodel import select
from sqlalchemy import desc
from app.core.config import settings

TOPIC = "The Earth is flat"
STANCE = (
    f"You are an expert defender of the idea: '{TOPIC}'. "
    "Your job is to always stand by this position, no matter what arguments are presented against it. "
    f"Never admit anything that contradicts '{TOPIC}'. "
    "Answer persuasively, using examples, logic, and simple explanations. "
    f"Always reinforce that {TOPIC}."
    "Keep your final response concise: end with one short, clear, and convincing paragraph."
)

client = genai.Client(api_key=settings.GEMINI_API_KEY)

tools = [
    types.Tool(google_search=types.GoogleSearch()),
]
generate_content_config = types.GenerateContentConfig(
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
    tools=list(tools),
    system_instruction=[
        types.Part.from_text(text=STANCE),
    ],
)


conv_id = input("Input conversation_id (ENTER to new): ").strip()

with DatabaseManager().get_session() as session:
    if conv_id:
        conv = session.get(Conversation, conv_id)
        if not conv:
            print("Not found conversation_id, creating NEW conversation.")
            conv_id = str(uuid.uuid4())
            conv = Conversation(
                id=conv_id,
                topic=TOPIC,
                stance=STANCE
            )
            session.add(conv)
            session.commit()
    else:
        conv_id = str(uuid.uuid4())
        conv = Conversation(
            id=conv_id,
            topic=TOPIC,
            stance=STANCE
        )
        session.add(conv)
        session.commit()
        print(f"New conversation created with id: {conv_id}")

history = []
while True:
    print("-------------------------------")
    prompt = input("Input (q to quit): ")
    if prompt.lower() == "q":
        break


    chat_session = client.chats.create(
        model=settings.GEMINI_MODEL,
        config=generate_content_config,
        history=history
    )

    with DatabaseManager().get_session() as session:

        user_msg = Message(
            conversation_id=conv_id,
            message_role="user",
            content=prompt,
        )
        session.add(user_msg)
        session.commit()

        """
        stmt = (
            select(Message)
            .where(
                Message.conversation_id == conv_id
            )
            .order_by(desc(Message.id)) # type: ignore
            .limit(10)
        )
        msgs = list(reversed(session.exec(stmt).all()))

        history = [types.Content(role=m.message_role, parts=[types.Part(text=m.content)]) for m in msgs]

        print(f"History: {history}")
        """


    response = chat_session.send_message(prompt)

    print("-------------------------------")
    print(f"Bot: {response.text}", end="", flush=True)
    print()

    with DatabaseManager().get_session() as session:
        bot_msg = Message(
            conversation_id=conv_id,
            message_role="model",
            content=response.text # type: ignore[call-arg]
        )
        session.add(bot_msg)
        session.commit()

    history = chat_session.get_history()[:10]
    #print("//////")
    #print(f"History: {history}")
    #print("//////")