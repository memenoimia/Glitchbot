import logging
import os
import threading
import time
import telegram
import requests
from config import Config
from telegram.ext import Updater
from dotenv import load_dotenv

load_dotenv()

# Initialize the bot and updater with environment variables
bot = telegram.Bot(token=Config.TELEGRAM_TOKEN)
updater = Updater(token=Config.TELEGRAM_TOKEN, use_context=True)

TOKEN_URL = f"{Config.BASE_URL}/token/v1/{Config.CHAIN_ID}/{Config.TOKEN_ADDRESS}"
TRADES_URL = f"{Config.BASE_URL}/trades/v1/latest/{Config.CHAIN_ID}/{Config.TOKEN_ADDRESS}"

# Configuration for logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Shared data dictionary to store fetched metrics
shared_data = {}

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
        logger.debug(f"Fetched trades data: {data}")  # Log the full response data
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
            logger.debug("Fetching and storing token data")
            fetch_and_store_token_data()
            
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

def fetch_latest_trades():
    try:
        response = requests.get(TRADES_URL)
        response.raise_for_status()
        trades = response.json()
        return trades
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching trades: {e}")
        return []

def notify_new_buy(trade):
    logging.debug(f"Received trade data: {trade}")

    # Ensure that token data has been fetched and stored
    if 'token_name' not in shared_data or 'token_url' not in shared_data:
        fetch_and_store_token_data()

    # Extracting data from the trade dictionary
    maker = trade.get('maker', 'N/A')
    truncated_maker = maker[:4] + "..." + maker[-4:]
    amount0 = int(float(trade.get('amount0', '0')))  # Convert to integer to remove decimal places
    amount1 = trade.get('amount1', 'N/A')
    price_usd = trade.get('priceUsd', 'N/A')
    volume_usd = trade.get('volumeUsd', 'N/A')
    token_name = shared_data.get('token_name', 'N/A')  # From token data
    token_url = shared_data.get('token_url', '')       # From token data
    website_url = shared_data.get('website_url', '')   # From token data
    dex_id = trade.get('dexId', 'N/A')
    block_number = trade.get('blockNumber', 'N/A')
    block_timestamp = trade.get('blockTimestamp', 'N/A')
    pair_id = trade.get('pairId', 'N/A')
    asset0_id = trade.get('asset0Id', 'N/A')
    asset1_id = trade.get('asset1Id', 'N/A')
    txn_id = trade.get('txnId', 'N/A')
    progress = trade.get('metadata', {}).get('progress', 'N/A')
    curve_position = trade.get('metadata', {}).get('curvePosition', 'N/A')

    # Log extracted values
    logging.debug(f"maker: {maker}")
    logging.debug(f"amount0: {amount0}")
    logging.debug(f"amount1: {amount1}")
    logging.debug(f"price_usd: {price_usd}")
    logging.debug(f"volume_usd: {volume_usd}")
    logging.debug(f"token_name: {token_name}")
    logging.debug(f"token_url: {token_url}")
    logging.debug(f"website_url: {website_url}")
    logging.debug(f"dex_id: {dex_id}")
    logging.debug(f"block_number: {block_number}")
    logging.debug(f"block_timestamp: {block_timestamp}")
    logging.debug(f"pair_id: {pair_id}")
    logging.debug(f"asset0_id: {asset0_id}")
    logging.debug(f"asset1_id: {asset1_id}")
    logging.debug(f"txn_id: {txn_id}")
    logging.debug(f"progress: {progress}")
    logging.debug(f"curve_position: {curve_position}")

    message = (
        f"👾👾👾 HEADROOM BUY! 👾👾👾\n"
        f"💵 Spent: ${volume_usd} 💰 Purchased: {amount0} {token_name}\n"
        f"👤 Wallet: <a href='https://solanabeach.io/address/{maker}'>{truncated_maker}</a>\n"
        f"🌙 <a href='{token_url}'>{dex_id}</a> 🔥 Progress: {progress}% 🌐 <a href='{website_url}')>Website</a>"
    )

    logging.info(f"Sending message: {message}")
    bot.send_message(chat_id=Config.TELEGRAM_CHAT_ID, text=message, parse_mode=telegram.ParseMode.HTML)

def main():
    trades = fetch_latest_trades()
    for trade in trades:
        notify_new_buy(trade)

if __name__ == "__main__":
    main()

# Start the check_new_buy_transaction function in a new thread
threading.Thread(target=check_new_buy_transaction, daemon=True).start()
