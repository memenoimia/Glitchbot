import logging
import requests
import threading
import time
import telegram
from news import get_latest_news
from telegram import Update, ParseMode, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from metrics import shared_data, fetch_and_store_token_data, fetch_and_store_latest_trades, get_latest_trades_for_token
from config import Config

# Initialize the bot with the Telegram token
bot = Bot(token=Config.TELEGRAM_TOKEN)

# Enable logging for the bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Function to send a message to the configured Telegram chat group
def send_message_to_group(message):
    try:
        bot.send_message(chat_id=Config.TELEGRAM_CHAT_ID, text=message)
        logger.info(f"Sent message to group: {message}")
    except Exception as e:
        logger.error(f"Error sending message to group: {e}")

# Command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Glitchbot! Use /help to see available commands.")
    send_message_to_group("Bot has started and is ready to receive commands.")

# Command handler for /help
def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "/start - Digital howdy! Beep boop!\n"
        "/headroom - HEADROOM token info. Get the skinny!\n"
        "/news - Latest Solana buzz. Extra, extra!\n"
        "/price - Current SOL price. Cha-ching!\n"
        "/subscribe - Future subscription awesomeness. Stay tuned!\n"
        "/transactions - Latest transactions. Splash!\n"
        "/marketcap - Market cap means big bucks?\n"
        "/volume24h - 24-hour volume. Big leagues!\n"
        "/change24h - 24-hour price change. Rollercoaster!\n"
        "/help - List of commands. Help is here!\n"
        "/whales - Large transactions. Whale watching!\n"
        "/chart [token_symbol] - Token price chart. Highs, lows, drama!\n"
    )
    update.message.reply_text(help_text)

# Command handler for /headroom
def headroom(update: Update, context: CallbackContext) -> None:
    try:
        fetch_and_store_token_data()
        token_data = shared_data['token_data']
        token_name = shared_data['token_name']
        token_symbol = shared_data['token_symbol']
        market_cap = float(shared_data['market_cap'])
        volume_24h = float(shared_data['volume_24h'])
        volume_6h = float(shared_data['volume_6h'])
        volume_1h = float(shared_data['volume_1h'])
        volume_5m = float(shared_data['volume_5m'])
        change_24h = float(shared_data['change_24h'])
        change_6h = float(shared_data['change_6h'])
        change_1h = float(shared_data['change_1h'])
        change_5m = float(shared_data['change_5m'])
        total_supply = shared_data['total_supply']
        current_price = float(shared_data['current_price'])
        banner_url = shared_data['token_banner']
        token_url = shared_data['token_url']
        website_url = shared_data['website_url']

        context.bot.send_photo(chat_id=update.effective_chat.id, photo=banner_url)

        message = (
            f"👾 Token: {token_name} ({token_symbol})\n"
            f"💸 Market Cap: ${market_cap:,.0f}\n"
            f"👟 Volume 24h: ${volume_24h:,.0f} 6h: ${volume_6h:,.0f} 1h: ${volume_1h:,.0f} 5m: {volume_5m:,.0f}\n"
            f"📈 Change 24h: {change_24h:.2f}% 6h: {change_6h:.2f}% 1h: {change_1h:.2f}% 5m: {change_5m:.2f}%\n"
            f"🏦 Total Supply: {total_supply} 💰Price: {current_price:.6f}\n"
            f"🌙 <a href='{token_url}'>Moonshot</a> 🌐 <a href='{website_url}'>Website</a>\n"
            f"<a href='https://solanabeach.io/address/{Config.TOKEN_ADDRESS}'>{Config.TOKEN_ADDRESS}</a>\n"
        )

        update.message.reply_text(message, parse_mode=ParseMode.HTML)
        logger.info("Displayed HEADROOM token information.")
    except Exception as e:
        logger.error(f"Error in headroom command: {e}")
        update.message.reply_text("An error occurred while fetching headroom information.")

# Command handler for /news
def news(update: Update, context: CallbackContext) -> None:
    try:
        news_items = get_latest_news()

        if not news_items:
            update.message.reply_text("No news available at the moment.")
            return

        news_message = "\n\n".join(
            [f"📰 <a href='{item['url']}'>{item['title']}</a>\n{item['description']}" for item in news_items[:3]]
        )
        update.message.reply_text(news_message, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error in news command: {e}")
        update.message.reply_text("An error occurred while fetching the latest news.")

# Command handler for /price
def price(update: Update, context: CallbackContext) -> None:
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
        response.raise_for_status()
        solana_price = response.json().get("solana", {}).get("usd", 0.0)
        
        message = f"💲 Current Solana Price: ${solana_price:.4f}"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in price command: {e}")
        update.message.reply_text("An error occurred while fetching the Solana price.")

# Command handler for /subscribe
def subscribe(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Subscription feature coming soon!")

# Command handler for /transactions
def transactions(update: Update, context: CallbackContext) -> None:
    try:
        fetch_and_store_token_data()
        latest_trades = get_latest_trades_for_token()

        if not latest_trades:
            update.message.reply_text("No recent transactions found.")
            return

        # Filter out only 'buy' transactions and sort by blockTimestamp
        buy_trades = [trade for trade in latest_trades if trade.get('type') == 'buy']
        if not buy_trades:
            update.message.reply_text("No recent buy transactions found.")
            return

        latest_trade = max(buy_trades, key=lambda trade: trade.get('blockTimestamp', 0))

        dex_id = latest_trade.get('dexId', 'N/A')
        block_number = latest_trade.get('blockNumber', 'N/A')
        block_timestamp = latest_trade.get('blockTimestamp', 'N/A')
        pair_id = latest_trade.get('pairId', 'N/A')
        asset0_id = latest_trade.get('asset0Id', 'N/A')
        asset1_id = latest_trade.get('asset1Id', 'N/A')
        txn_id = latest_trade.get('txnId', 'N/A')
        maker = latest_trade.get('maker', 'N/A')
        txn_type = latest_trade.get('type', 'N/A')
        amount0 = int(float(latest_trade.get('amount0', 0)))  # Convert amount0 to integer
        amount1 = latest_trade.get('amount1', 'N/A')
        price_native = latest_trade.get('priceNative', 'N/A')
        price_usd = latest_trade.get('priceUsd', 'N/A')
        volume_usd = latest_trade.get('volumeUsd', 'N/A')
        metadata = latest_trade.get('metadata', {})
        progress = metadata.get('progress', 'N/A')
        curve_position = latest_trade.get('curvePosition', 'N/A')

        token_name = shared_data.get('token_name', 'N/A')
        token_url = shared_data.get('token_url', '')
        website_url = shared_data.get('website_url', '')

        context.bot.send_video(
            chat_id=update.effective_chat.id,
            video='https://cdn.glitch.global/ffa82557-90ab-436a-9585-9e6791f55285/582b8583-2440-4c96-aa3e-6de061b74b86.mp4?v=1721053375683'
        )
        
        message = (
            f"👾👾👾 HEADROOM BUY! 👾👾👾\n"
            f"💵 Spent: ${volume_usd} 💰 Purchased: {amount0} {token_name}\n"
            f"👤 Wallet: <a href='https://solanabeach.io/address/{maker}'>{maker[:4]}...{maker[-4:]}</a>\n"
            f"🌙 <a href='{token_url}'>Moonshot</a> 🔥 Progress: {progress}% 🌐 <a href='{website_url}'>Website</a>\n"
            f"<a href='https://solanabeach.io/address/{pair_id}'>{pair_id}</a>\n"
        )

        update.message.reply_text(message, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error in transactions command: {e}")
        update.message.reply_text("An error occurred while fetching transactions information.")

# Command handler for /marketcap
def marketcap(update: Update, context: CallbackContext) -> None:
    try:
        market_cap = float(shared_data.get('market_cap', 0.0))
        message = f"💸 Market Cap: ${market_cap:,.0f}"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in marketcap command: {e}")
        update.message.reply_text("An error occurred while fetching the market cap.")

# Command handler for /volume24h
def volume24h(update: Update, context: CallbackContext) -> None:
    try:
        volume_24h = float(shared_data.get('volume_24h', 0.0))
        message = f"🔄 Volume 24h: ${volume_24h:,.0f}"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in volume24h command: {e}")
        update.message.reply_text("An error occurred while fetching the 24h volume.")

# Command handler for /change24h
def change24h(update: Update, context: CallbackContext) -> None:
    try:
        change_24h = float(shared_data.get('change_24h', 0.0))
        message = f"📈 Change 24h: {change_24h:.2f}%"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in change24h command: {e}")
        update.message.reply_text("An error occurred while fetching the 24h change.")

# Command handler for /whales
def whales(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Feature coming soon!")

# Command handler for /chart
def chart(update: Update, context: CallbackContext) -> None:
    token_symbol = ' '.join(context.args).upper()
    if not token_symbol:
        update.message.reply_text("Please specify a token symbol. Usage: /chart [token_symbol]")
        return
    update.message.reply_text(f"Token price chart for {token_symbol}. Highs, lows, drama!")

# Function to set up the bot and add command handlers
def main() -> None:
    updater = Updater(Config.TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("headroom", headroom))
    dispatcher.add_handler(CommandHandler("news", news))
    dispatcher.add_handler(CommandHandler("price", price))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    dispatcher.add_handler(CommandHandler("transactions", transactions))
    dispatcher.add_handler(CommandHandler("marketcap", marketcap))
    dispatcher.add_handler(CommandHandler("volume24h", volume24h))
    dispatcher.add_handler(CommandHandler("change24h", change24h))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("whales", whales))
    dispatcher.add_handler(CommandHandler("chart", chart, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # Run the bot
    main()
