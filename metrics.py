import requests
from config import Config

BASE_URL = f"https://api.moonshot.cc/token/v1/solana/{Config.TOKEN_ADDRESS}"

def get_token_data():
    response = requests.get(BASE_URL)
    return response.json()

def get_token_name():
    data = get_token_data()
    return data.get('baseToken', {}).get('name', 'N/A')

def get_token_symbol():
    data = get_token_data()
    return data.get('baseToken', {}).get('symbol', 'N/A')

def get_market_cap():
    data = get_token_data()
    return data.get('marketCap', 0.0)

def get_24h_volume():
    data = get_token_data()
    return data.get('volume', {}).get('h24', {}).get('total', 0.0)

def get_6h_volume():
    data = get_token_data()
    return data.get('volume', {}).get('h6', {}).get('total', 0.0)

def get_1h_volume():
    data = get_token_data()
    return data.get('volume', {}).get('h1', {}).get('total', 0.0)

def get_5m_volume():
    data = get_token_data()
    return data.get('volume', {}).get('m5', {}).get('total', 0.0)

def get_24h_change():
    data = get_token_data()
    return data.get('priceChange', {}).get('h24', 0.0)

def get_6h_change():
    data = get_token_data()
    return data.get('priceChange', {}).get('h6', 0.0)

def get_1h_change():
    data = get_token_data()
    return data.get('priceChange', {}).get('h1', 0.0)

def get_5m_change():
    data = get_token_data()
    return data.get('priceChange', {}).get('m5', 0.0)

def get_total_supply():
    data = get_token_data()
    return data.get('totalSupply', 'N/A')

def get_liquidity():
    data = get_token_data()
    return data.get('liquidity', {}).get('h24', {}).get('total', 0.0)

def get_latest_trades_for_token():
    url = f"https://api.moonshot.cc/trades/v1/latest/{Config.CHAIN_ID}/{Config.TOKEN_ADDRESS}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get('data', [])

def get_token_banner():
    data = get_token_data()
    return data.get('profile', {}).get('banner', '')

def get_token_creator():
    data = get_token_data()
    return data.get('moonshot', {}).get('creator', '')

def get_token_url():
    data = get_token_data()
    return data.get('url', '')

def get_current_price():
    data = get_token_data()
    return data.get('priceUsd', 0.0)
