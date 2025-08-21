from typing import Literal

ROLE_MAP: dict[str, Literal["user", "bot"]] = {
    "user": "user",
    "model": "bot"
}

MIN_TOPIC_LENGTH = 5
MIN_STANCE_LENGTH = 20

MIN_MESSAGE_LIMIT = 1
MAX_MESSAGE_LIMIT = 100
