import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from transactions import get_recent_transactions, get_sol_price
from news import get_latest_news
from metrics import get_market_cap, get_change_24h
from config import TELEGRAM_TOKEN, HEADROOM_IMAGE_URL, TOKEN_ADDRESS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /help to see available commands.')
    logger.info("Started bot interaction.")

def help_command(update: Update, context: CallbackContext) -> None:
    help_message = """
Available Commands:
/headroom - Get the scoop on the HEADROOM token. It's a doozy!
/news - Latest buzz about Solana. Hot off the press!
/price - Current SOL price. Cha-ching!
/subscribe - Get price alerts. Stay in the loop!
/transactions - Latest moves glitch. Who's doing what?
/marketcap - Current market capitalization of your token. Big numbers!
/volume24h - 24-hour trading volume. How much action?
/change24h - 24-hour price change. Up or down?
/help - Need help? I'm here to assist!
    """
    update.message.reply_text(help_message)
    logger.info("Displayed help message.")

def headroom(update: Update, context: CallbackContext) -> None:
    try:
        transactions = get_recent_transactions()
        if not transactions:
            update.message.reply_text("No recent transactions found.")
            logger.info("No recent transactions found.")
            return

        latest_transaction = transactions[0]
        amount_token = latest_transaction.get('amountToken', 'N/A')
        usd_amount = latest_transaction.get('usdAmount', 'N/A')
        sol_amount = latest_transaction.get('solAmount', 'N/A')
        truncated_wallet = f"{latest_transaction['signer'][:6]}...{latest_transaction['signer'][-6:]}"

        market_cap = get_market_cap()
        change_24h = get_change_24h()

        headroom_message = f"""
🗣 HEADROOM:

💵 Spent: ${usd_amount:.2f} ({sol_amount:.4f} SOL)
🪙 Position: {change_24h:.2f}%
💸 Market Cap: ${market_cap:.2f}
👤 Wallet: [{truncated_wallet}](https://solanabeach.io/address/{latest_transaction['signer']})
💰 $HEADROOM Purchased: {amount_token}
🌙 [Moonshot](https://dexscreener.com/solana/{TOKEN_ADDRESS})
🌐 [Website](https://memenoimia.fun)
        """
        update.message.reply_text(headroom_message, parse_mode="Markdown")
        logger.info("Displayed HEADROOM token information.")
    except Exception as e:
        logger.exception("Error in headroom command")

def news(update: Update, context: CallbackContext) -> None:
    try:
        latest_news = get_latest_news()
        if not latest_news:
            update.message.reply_text("No news found.")
            logger.info("No news found.")
            return

        news_message = "\n\n".join([f"{news_item['title']}\n{news_item['url']}" for news_item in latest_news])
        update.message.reply_text(news_message)
        logger.info("Displayed latest news.")
    except Exception as e:
        logger.exception("Error in news command")

def price(update: Update, context: CallbackContext) -> None:
    try:
        sol_price = get_sol_price()
        price_message = f"Current SOL price: ${sol_price:.2f}"
        update.message.reply_text(price_message)
        logger.info("Displayed current SOL price.")
    except Exception as e:
        logger.exception("Error in price command")

def subscribe(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Subscription feature is not implemented yet.")
    logger.info("Subscription feature is not implemented yet.")

def transactions(update: Update, context: CallbackContext) -> None:
    try:
        transactions = get_recent_transactions()
        if not transactions:
            update.message.reply_text("No recent transactions found.")
            logger.info("No recent transactions found.")
            return

        transactions_message = "\n\n".join([f"Transaction: {tx['id']}, Amount: {tx['amount']}" for tx in transactions])
        update.message.reply_text(transactions_message)
        logger.info("Displayed recent transactions.")
    except Exception as e:
        logger.exception("Error in transactions command")

def marketcap(update: Update, context: CallbackContext) -> None:
    try:
        market_cap = get_market_cap()
        marketcap_message = f"Current market capitalization: ${market_cap:.2f}"
        update.message.reply_text(marketcap_message)
        logger.info("Displayed market capitalization.")
    except Exception as e:
        logger.exception("Error in marketcap command")

def volume24h(update: Update, context: CallbackContext) -> None:
    try:
        volume_24h = get_volume_24h()
        volume_message = f"24-hour trading volume: ${volume_24h:.2f}"
        update.message.reply_text(volume_message)
        logger.info("Displayed 24-hour trading volume.")
    except Exception as e:
        logger.exception("Error in volume24h command")

def change24h(update: Update, context: CallbackContext) -> None:
    try:
        change_24h = get_change_24h()
        change_message = f"24-hour price change: {change_24h:.2f}%"
        update.message.reply_text(change_message)
        logger.info("Displayed 24-hour price change.")
    except Exception as e:
        logger.exception("Error in change24h command")

def process_update(update_dict, dispatcher):
    logger.info(f"Update received: {update_dict}")
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        update = Update.de_json(update_dict, bot)
        context = CallbackContext(dispatcher)

        if update.message:
            text = update.message.text
            if text == "/start":
                start(update, context)
            elif text == "/help":
                help_command(update, context)
            elif text == "/headroom":
                headroom(update, context)
            elif text == "/news":
                news(update, context)
            elif text == "/price":
                price(update, context)
            elif text == "/subscribe":
                subscribe(update, context)
            elif text == "/transactions":
                transactions(update, context)
            elif text == "/marketcap":
                marketcap(update, context)
            elif text == "/volume24h":
                volume24h(update, context)
            elif text == "/change24h":
                change24h(update, context)
    except Exception as e:
        logger.exception("Error handling the update")

def main() -> Updater:
    logger.info(f"Using TELEGRAM_TOKEN: {TELEGRAM_TOKEN}")

    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("headroom", headroom))
    dispatcher.add_handler(CommandHandler("news", news))
    dispatcher.add_handler(CommandHandler("price", price))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    dispatcher.add_handler(CommandHandler("transactions", transactions))
    dispatcher.add_handler(CommandHandler("marketcap", marketcap))
    dispatcher.add_handler(CommandHandler("volume24h", volume24h))
    dispatcher.add_handler(CommandHandler("change24h", change24h))

    updater.start_polling()
    logger.info("Bot started.")
    updater.idle()

    return updater

if __name__ == "__main__":
    main()
