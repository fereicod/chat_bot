from typing import Any
from google.genai import types


TEMPERATURE = 0
THINKING_BUDGET = -1
GEMINI_SAFETY_SETTINGS = [
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
]
TOOLS: list[Any] = [
    types.Tool(google_search=types.GoogleSearch()),
]

GENERATE_CONTENT_CONFIG = types.GenerateContentConfig(
    temperature=TEMPERATURE,
    thinking_config=types.ThinkingConfig(thinking_budget=THINKING_BUDGET),
    safety_settings=GEMINI_SAFETY_SETTINGS,
    tools=TOOLS,
    system_instruction=[],
)