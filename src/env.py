from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_SECRET = os.getenv("BOT_SECRET")
EXTENSION = os.getenv("EXTENSION")
print(EXTENSION)

if not (API_KEY and BOT_SECRET and BOT_TOKEN):
    raise Exception("not enough env exception")
