import requests
import logging
from config import TOKEN_ADDRESS, SOLANABEACH_API

# Setup logging
logger = logging.getLogger(__name__)

BASE_URL = "https://api.solanabeach.io/v1"

def get_recent_transactions():
    url = f"{BASE_URL}/account/{TOKEN_ADDRESS}/transactions"
    headers = {"Authorization": f"Bearer {SOLANABEACH_API}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        transactions = response.json()
        logger.debug(f"Transactions data: {transactions}")
        return transactions
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching transactions: {e}")
        return []

def get_sol_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()
        price_data = response.json()
        sol_price = price_data["solana"]["usd"]
        logger.debug(f"SOL price data: {sol_price}")
        return sol_price
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching SOL price: {e}")
        return None
