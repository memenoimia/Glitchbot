import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    NEWS_API_KEY = os.getenv('NEWS_TOKEN')
    TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS')
    CHAIN_ID = 'solana'
    MOONSHOT_API_BASE = 'https://api.moonshot.cc'
    TOKEN_CREATOR_ADDRESS = os.getenv('TOKEN_CREATOR_ADDRESS')
    BOND_CURVE_ADDRESS = os.getenv('BOND_CURVE_ADDRESS')
