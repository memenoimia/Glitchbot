# config.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BASE_URL = os.getenv('BASE_URL')
GLITCH_WEBHOOK = os.getenv('GLITCH_WEBHOOK')
CONVOY_URL = os.getenv('CONVOY_URL')
CONVOY_OWNER_ID = os.getenv('CONVOY_OWNER_ID')
CONVOY_ENDPOINT_SECRET = os.getenv('CONVOY_ENDPOINT_SECRET')
CONVOY_API = os.getenv('CONVOY_API')
SOLANABEACH_API = os.getenv('SOLANABEACH_API')
BLOCKDAEMON_API = os.getenv('BLOCKDAEMON_API')
NEWS_TOKEN = os.getenv('NEWS_TOKEN')
TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS')
HEADROOM_IMAGE_URL = os.getenv('HEADROOM_IMAGE_URL')
