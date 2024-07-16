import logging
import os
import threading
import time
import telegram
import requests
from config import Config

# Configuration for logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Log message format
    level=logging.DEBUG  # Log level set to DEBUG (logs all levels: DEBUG and above)
)
logger = logging.getLogger(__name__)  # Create a logger with the name of the current module

# Shared data dictionary to store fetched metrics
shared_data = {}

TOKEN_URL = f"{Config.BASE_URL}/token/v1/{Config.CHAIN_ID}/{Config.TOKEN_ADDRESS}"
TRADES_URL = f"{Config.BASE_URL}/trades/v1/latest/{Config.CHAIN_ID}/{Config.TOKEN_ADDRESS}"

def fetch_and_store_token_data():
    try:
        response = requests.get(TOKEN_URL)
        response.raise_for_status()
        data = response.json()
        
        shared_data['token_data'] = data
        shared_data['token_name'] = data.get('baseToken', {}).get('name', 'N/A')
        shared_data['token_symbol'] = data.get('baseToken', {}).get('symbol', 'N/A')
        shared_data['market_cap'] = data.get('marketCap', 0.0)
        shared_data['volume_24h'] = data.get('volume', {}).get('h24', {}).get('total', 0.0)
        shared_data['volume_6h'] = data.get('volume', {}).get('h6', {}).get('total', 0.0)
        shared_data['volume_1h'] = data.get('volume', {}).get('h1', {}).get('total', 0.0)
        shared_data['volume_5m'] = data.get('volume', {}).get('m5', {}).get('total', 0.0)
        shared_data['change_24h'] = data.get('priceChange', {}).get('h24', 0.0)
        shared_data['change_6h'] = data.get('priceChange', {}).get('h6', 0.0)
        shared_data['change_1h'] = data.get('priceChange', {}).get('h1', 0.0)
        shared_data['change_5m'] = data.get('priceChange', {}).get('m5', 0.0)
        shared_data['total_supply'] = data.get('totalSupply', '1B')
        shared_data['current_price'] = data.get('priceUsd', 0.0)
        shared_data['token_banner'] = data.get('profile', {}).get('banner', '')
        shared_data['token_url'] = data.get('url', '')
        shared_data['website_url'] = data.get('profile', {}).get('links', [''])[0]
        logger.info("Token data fetched and stored successfully.")
    except Exception as e:
        logger.error(f"Error fetching token data: {e}")

def fetch_and_store_latest_trades():
    try:
        response = requests.get(TRADES_URL)
        response.raise_for_status()
        data = response.json()
        shared_data['latest_trades'] = data
        logger.info("Latest trades fetched and stored successfully.")
    except Exception as e:
        logger.error(f"Error fetching latest trades: {e}")

def get_latest_trades_for_token():
    fetch_and_store_latest_trades()
    return shared_data.get('latest_trades', [])

# Function to check for new buy transactions
last_transaction_timestamp = None

def check_new_buy_transaction():
    global last_transaction_timestamp
    while True:
        try:
            logger.debug("Fetching and storing latest trades")
            fetch_and_store_latest_trades()
            latest_trades = shared_data.get('latest_trades', [])
            for trade in latest_trades:
                logger.debug(f"Processing trade: {trade}")
                if 'blockTimestamp' not in trade:
                    logger.warning(f"Trade missing 'blockTimestamp' key: {trade}")
                    continue
                if trade['type'] == 'buy' and (last_transaction_timestamp is None or trade['blockTimestamp'] > last_transaction_timestamp):
                    logger.info(f"New buy transaction found: {trade}")
                    notify_new_buy(trade)
                    last_transaction_timestamp = trade['blockTimestamp']
                    break
        except Exception as e:
            logger.error(f"Error in check_new_buy_transaction: {e}")
        time.sleep(60)  # Check every 60 seconds

# Function to send a notification for a new buy transaction
def notify_new_buy(trade):
    try:
        bot = telegram.Bot(token=Config.TELEGRAM_TOKEN)
        bot.send_message(chat_id=Config.TELEGRAM_CHAT_ID, text="NEW BUY!")
        logger.info(f"Notification sent for new buy transaction: {trade}")
    except Exception as e:
        logger.error(f"Error in notify_new_buy: {e}")

# Start the check_new_buy_transaction function in a new thread
threading.Thread(target=check_new_buy_transaction, daemon=True).start()
