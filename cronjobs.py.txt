import logging
from transactions import get_recent_transactions, get_sol_price
from config import HEADROOM_IMAGE_URL, TOKEN_ADDRESS, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
from telegram import Bot

logging.basicConfig(level=logging.INFO)

def monitor_transactions(bot: Bot):
    try:
        transactions = get_recent_transactions()
        logging.info(f"Fetched transactions: {transactions}")

        if not transactions:
            logging.info("No recent transactions found.")
            return

        latest_transaction = transactions[0]
        amount_token = latest_transaction.get('amountToken', 'N/A')
        usd_amount = latest_transaction.get('usdAmount', 'N/A')
        sol_amount = latest_transaction.get('solAmount', 'N/A')
        truncated_wallet = f"{latest_transaction['signer'][:6]}...{latest_transaction['signer'][-6:]}"

        transaction_message = f"""
🗣 HEADROOM:

💵 Spent: ${usd_amount:.2f} ({sol_amount:.4f} SOL)
👤 Wallet: [{truncated_wallet}](https://solanabeach.io/address/{latest_transaction['signer']})
💰 $HEADROOM Purchased: {amount_token}
🌙 [Moonshot](https://dexscreener.com/solana/{TOKEN_ADDRESS})
🌐 [Website](https://memenoimia.fun)
        """
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=HEADROOM_IMAGE_URL, caption=transaction_message, parse_mode="Markdown")
        logging.info("Displayed latest transaction.")
    except Exception as e:
        logging.error(f"Error fetching recent transactions: {e}")

def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    monitor_transactions(bot)

if __name__ == "__main__":
    main()
