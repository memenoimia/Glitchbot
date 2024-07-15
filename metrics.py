import requests
from config import Config

# Shared data dictionary to store fetched metrics
shared_data = {}

TOKEN_URL = f"{Config.BASE_URL}/token/v1/{Config.CHAIN_ID}/{Config.TOKEN_ADDRESS}"

def fetch_and_store_token_data():
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
    shared_data['total_supply'] = data.get('totalSupply', 'N/A')
    shared_data['liquidity'] = data.get('liquidity', {}).get('h24', {}).get('total', 0.0)
    shared_data['current_price'] = data.get('priceUsd', 0.0)
    shared_data['token_banner'] = data.get('profile', {}).get('banner', '')
    shared_data['token_url'] = data.get('url', '')
    shared_data['website_url'] = data.get('profile', {}).get('links', [''])[0]

def get_latest_trades_for_token():
    url = f"{Config.BASE_URL}/trades/v1/latest/{Config.CHAIN_ID}/{Config.TOKEN_ADDRESS}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
