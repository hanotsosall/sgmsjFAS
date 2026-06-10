import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
    FLUX_MODEL = os.getenv("FLUX_MODEL", "black-forest-labs/flux-schnell")
    WEBAPP_URL = os.getenv("WEBAPP_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Экономика
    ENERGY_COST_PER_MESSAGE = 1
    GEMS_COST_PER_IMAGE = 5
    DEFAULT_ENERGY = 30
    ENERGY_REFILL_PRICE_STARS = 10   # 10 Stars за +20 энергии
    GEMS_PACKS = {
        50: 25,    # 25 Stars -> 50 Gems
        200: 90,
        1000: 400
    }

config = Config()