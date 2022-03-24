import os
import dotenv

from app.logger import get_logger

log = get_logger(__name__)


if dotenv_file := dotenv.find_dotenv():
    log.warning(f"Loading .env file from {dotenv_file}")
    dotenv.load_dotenv()
else:
    log.error("Could not find/open .env file")


LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)  # example: 'mysql://user:pass@localhost:3306/db'

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [  # put rest of the models as so in the list
                "app.models.user",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}

MODE = os.getenv("MODE", "webhook")  # 'webhook' or 'polling'

PARSE_MODE = os.getenv("PARSE_MODE", "Html")  # 'Html' or 'MarkdownV2'

PROXY = os.getenv("PROXY_URL", None)  # example: 'socks5://127.0.0.1:1080'

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_FSM_DB = int(os.getenv("REDIS_FSM_DB", 1))

WEBHOOK_HOST = os.getenv("WEBHOOK_PATH")  # example: 'https://domain.com'
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")  # example: '/webhook'
WEBHOOK_URL = os.getenv(f"{WEBHOOK_HOST}{WEBHOOK_PATH}")

WEBAPP_HOST = os.getenv("WEBAPP_HOST", "localhost")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", 3001))
