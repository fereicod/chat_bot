import logging
import sys

logging.getLogger("chatbot_logger").handlers.clear()

logger = logging.getLogger("chatbot_logger")
logger.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stdout)

# timestamp, level, module and message
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - [%(module)s:%(funcName)s:%(lineno)d] - %(message)s'
)
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)