import requests
from config import Config

# Fetch token data from Moonshot API
def get_token_data():
    url = f"{Config.MOONSHOT_API_BASE}/token/v1/{Config.CHAIN_ID}/{Config.TOKEN_ADDRESS}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Fetch latest trades for a specified token
def get_latest_trades_for_token():
    url = f"{Config.MOONSHOT_API_BASE}/trades/v1/latest/{Config.CHAIN_ID}/{Config.TOKEN_ADDRESS}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get('data', [])

# Fetch current price from token data
def get_current_price():
    token_data = get_token_data()
    return token_data.get('priceUsd', 0.0)

# Fetch token name from token data
def get_token_name():
    token_data = get_token_data()
    return token_data.get('baseToken', {}).get('name', 'N/A')

# Fetch token symbol from token data
def get_token_symbol():
    token_data = get_token_data()
    return token_data.get('baseToken', {}).get('symbol', 'N/A')

# Fetch market cap from token data
def get_market_cap():
    token_data = get_token_data()
    return token_data.get('marketCap', 0.0)

# Fetch 24-hour volume from token data
def get_24h_volume():
    token_data = get_token_data()
    return token_data.get('volume', {}).get('h24', {}).get('total', 0.0)

# Fetch 6-hour volume from token data
def get_6h_volume():
    token_data = get_token_data()
    return token_data.get('volume', {}).get('h6', {}).get('total', 0.0)

# Fetch 1-hour volume from token data
def get_1h_volume():
    token_data = get_token_data()
    return token_data.get('volume', {}).get('h1', {}).get('total', 0.0)

# Fetch 5-minute volume from token data
def get_5m_volume():
    token_data = get_token_data()
    return token_data.get('volume', {}).get('m5', {}).get('total', 0.0)

# Fetch 24-hour price change from token data
def get_24h_change():
    token_data = get_token_data()
    return token_data.get('priceChange', {}).get('h24', 0.0)

# Fetch 6-hour price change from token data
def get_6h_change():
    token_data = get_token_data()
    return token_data.get('priceChange', {}).get('h6', 0.0)

# Fetch 1-hour price change from token data
def get_1h_change():
    token_data = get_token_data()
    return token_data.get('priceChange', {}).get('h1', 0.0)

# Fetch 5-minute price change from token data
def get_5m_change():
    token_data = get_token_data()
    return token_data.get('priceChange', {}).get('m5', 0.0)

# Fetch total supply from token data
def get_total_supply():
    token_data = get_token_data()
    return token_data.get('totalSupply', 'N/A')

# Fetch liquidity from token data
def get_liquidity():
    token_data = get_token_data()
    return token_data.get('liquidity', {}).get('h24', {}).get('total', 0.0)

# Get token creator address
def get_token_creator():
    token_data = get_token_data()
    return token_data.get('moonshot', {}).get('creator', '')

# Get token banner URL
def get_token_banner():
    token_data = get_token_data()
    return token_data.get('profile', {}).get('banner', '')

# Get token URL
def get_token_url():
    token_data = get_token_data()
    return token_data.get('url', '')
