import requests
import logging
from config import SOLANABEACH_API, TOKEN_ADDRESS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_market_cap():
    try:
        url = f"https://api.solanabeach.io/v1/account/{TOKEN_ADDRESS}/market_cap"
        headers = {
            'Authorization': f'Bearer {SOLANABEACH_API}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        market_cap = data['marketCap']
        return market_cap
    except Exception as e:
        logger.error(f"Error fetching market cap: {e}")
        return None

def get_volume_24h():
    try:
        url = f"https://api.solanabeach.io/v1/account/{TOKEN_ADDRESS}/volume_24h"
        headers = {
            'Authorization': f'Bearer {SOLANABEACH_API}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        volume_24h = data['volume_24h']
        return volume_24h
    except Exception as e:
        logger.error(f"Error fetching 24-hour volume: {e}")
        return None

def get_change_24h():
    try:
        url = f"https://api.solanabeach.io/v1/account/{TOKEN_ADDRESS}/change_24h"
        headers = {
            'Authorization': f'Bearer {SOLANABEACH_API}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        change_24h = data['change_24h']
        return change_24h
    except Exception as e:
        logger.error(f"Error fetching 24-hour price change: {e}")
        return None
