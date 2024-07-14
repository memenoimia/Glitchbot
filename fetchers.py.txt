import requests
import logging
from config import TOKEN_ADDRESS, SOLANABEACH_API

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def get_sol_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd')
        response.raise_for_status()
        price_data = response.json()
        sol_price = price_data['solana']['usd']
        return sol_price
    except Exception as e:
        logger.error(f"Error fetching SOL price: {e}")
        return None

def get_recent_transactions():
    try:
        url = f"https://api.solanabeach.io/v1/account/{TOKEN_ADDRESS}/transactions?limit=1"
        headers = {
            'Authorization': f'Bearer {SOLANABEACH_API}',
            'Content-Type': 'application/json'
        }
        logger.debug(f"Fetching transactions with URL: {url}")
        response = requests.get(url, headers=headers)
        logger.debug(f"Response status code: {response.status_code}")
        response.raise_for_status()
        
        transactions = response.json()
        logger.info(f"Transactions fetched: {transactions}")

        sol_price = get_sol_price()
        if sol_price is None:
            logger.error("Could not fetch SOL price.")
            return []

        formatted_transactions = []
        for tx in transactions:
            try:
                if 'postTokenBalances' in tx['meta'] and tx['meta']['postTokenBalances']:
                    balance = tx['meta']['postTokenBalances'][0]
                    amount_token = balance['uiTokenAmount']['uiAmount']
                    amount_token_in_sol = float(amount_token) / 10**9  # Assuming token amount is in lamports
                    usd_amount = amount_token_in_sol * sol_price
                    signer = balance['owner']['address']
                    transaction = {
                        'amountToken': amount_token,
                        'usdAmount': usd_amount,
                        'signer': signer
                    }
                    formatted_transactions.append(transaction)
                else:
                    logger.warning(f"No postTokenBalances in transaction: {tx}")
            except KeyError as e:
                logger.error(f"KeyError: {e} in transaction {tx}")
        
        return formatted_transactions
    except Exception as e:
        logger.error(f"Error fetching recent transactions: {e}")
        return []
