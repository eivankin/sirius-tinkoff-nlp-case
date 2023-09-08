import os

TOKEN = os.getenv("BOT_API_TOKEN")
REDIS_URL = os.getenv("REDIS_URL", default="redis://localhost")
MODEL_URL = os.getenv("MODEL_URL")
