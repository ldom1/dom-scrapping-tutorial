import sys
import os
from dotenv import find_dotenv, load_dotenv
from loguru import logger

from dom_scrapping_tutorial import constant


# Load environment variables
load_dotenv(find_dotenv())

# Logger
# Here, we incorporate {process} into the default format
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> |<red> PID {process}</red> | <level>{level: <8}</level>| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=os.getenv("LOG_LEVEL", "INFO"),
)

# Environment variables
RUN_ENV = os.environ.get("RUN_ENV", constant.RUN_ENV_LOCAL)
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", None)
