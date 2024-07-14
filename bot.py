import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from metrics import (
    get_token_name,
    get_token_symbol,
    get_market_cap,
    get_24h_volume,
    get_6h_volume,
    get_1h_volume,
    get_5m_volume,
    get_24h_change,
    get_6h_change,
    get_1h_change,
    get_5m_change,
    get_total_supply,
    get_liquidity,
    get_token_data,
    get_token_banner,
    get_token_url,
    get_current_price,
    get_latest_trades_for_token
)
from config import Config
from news import get_latest_news

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Glitchbot! Use /help to see available commands.")

# Define the command handler for /help
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

# Define the command handler for /headroom
def headroom(update: Update, context: CallbackContext) -> None:
    try:
        token_data = get_token_data()
        token_name = get_token_name()
        token_symbol = get_token_symbol()
        market_cap = float(get_market_cap())
        volume_24h = float(get_24h_volume())
        volume_6h = float(get_6h_volume())
        volume_1h = float(get_1h_volume())
        volume_5m = float(get_5m_volume())
        change_24h = float(get_24h_change())
        change_6h = float(get_6h_change())
        change_1h = float(get_1h_change())
        change_5m = float(get_5m_change())
        total_supply = get_total_supply()
        liquidity = float(get_liquidity())
        current_price = float(get_current_price())
        banner_url = get_token_banner()
        token_url = get_token_url()

        # Get the first URL from the links
        website_url = token_data.get('profile', {}).get('links', [''])[0]

        # Send the banner image
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=banner_url)

        # Prepare the message
        message = (
            f"🌐 Token: {token_name} ({token_symbol})\n"
            f"{Config.TOKEN_ADDRESS}\n"
            f"💸 Market Cap: ${market_cap:,.0f}\n"
            f"🔄 Volume 24h: ${volume_24h:,.0f} 6h: ${volume_6h:,.0f} 1h: ${volume_1h:,.0f} 5m: ${volume_5m:,.0f}\n"
            f"📈 Change 24h: {change_24h:.2f}% 6h: {change_6h:.2f}% 1h: {change_1h:.2f}% 5m: {change_5m:.2f}%\n"
            f"🏦 Total Supply: {total_supply} 💧 Liquidity: ${liquidity:,.0f}\n"
            f"🌙 <a href='{token_url}'>Moonshot</a> 🌐 <a href='{website_url}'>Website</a>"
        )

        # Send the message with the token information
        update.message.reply_text(message, parse_mode=ParseMode.HTML)
        logger.info("Displayed HEADROOM token information.")
    except Exception as e:
        logger.error(f"Error in headroom command: {e}")
        update.message.reply_text("An error occurred while fetching headroom information.")

# Define the command handler for /news
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

# Define the command handler for /price
def price(update: Update, context: CallbackContext) -> None:
    try:
        current_price = get_current_price()
        message = f"💲 Current Price: ${current_price:.4f}"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in price command: {e}")
        update.message.reply_text("An error occurred while fetching the current price.")

# Define the command handler for /subscribe
def subscribe(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Subscription feature coming soon!")

# Define the command handler for /transactions
def transactions(update: Update, context: CallbackContext) -> None:
    try:
        latest_trades = get_latest_trades_for_token()
        if not latest_trades:
            update.message.reply_text("No recent transactions found.")
            return

        latest_buy = next((trade for trade in latest_trades if trade.get('type') == 'buy'), None)
        if latest_buy:
            volume_usd = latest_buy.get('volumeUsd', 'N/A')
            amount0 = latest_buy.get('amount0', 'N/A')
            total_txns = len(latest_trades)
            wallet = latest_buy.get('wallet', 'N/A')
            progress = latest_buy.get('progress', 'N/A')
            solscan_url = f"https://solscan.io/tx/{latest_buy.get('txHash', '')}"

            message = (
                f"$Headroom Buy!\n\n"
                f"👾👾👾👾👾👾\n\n"
                f"💵 Spent: ${volume_usd}\n"
                f"👾 Purchased: {amount0} MAX\n"
                f"🛣 Total Txns: {total_txns}\n"
                f"👤 Wallet: {wallet}\n"
                f"🌙 Moonshot Progress: {progress}%\n"
                f"🌤 <a href='{solscan_url}'>Solscan</a>\n"
                f"🌐 <a href='{website_url}'>Website</a>"
            )

            # Send the message with the latest trade information
            update.message.reply_text(message, parse_mode=ParseMode.HTML)
            logger.info("Displayed latest trade information.")
        else:
            update.message.reply_text("No recent buy transactions found.")
            logger.info("No recent buy transactions found.")
    except Exception as e:
        logger.error(f"Error in transactions command: {e}")
        update.message.reply_text("An error occurred while fetching transactions information.")

# Define the command handler for /marketcap
def marketcap(update: Update, context: CallbackContext) -> None:
    try:
        market_cap = get_market_cap()
        message = f"💸 Market Cap: ${market_cap:,.0f}"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in marketcap command: {e}")
        update.message.reply_text("An error occurred while fetching the market cap.")

# Define the command handler for /volume24h
def volume24h(update: Update, context: CallbackContext) -> None:
    try:
        volume_24h = get_24h_volume()
        message = f"🔄 Volume 24h: ${volume_24h:,.0f}"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in volume24h command: {e}")
        update.message.reply_text("An error occurred while fetching the 24h volume.")

# Define the command handler for /change24h
def change24h(update: Update, context: CallbackContext) -> None:
    try:
        change_24h = get_24h_change()
        message = f"📈 Change 24h: {change_24h:.2f}%"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in change24h command: {e}")
        update.message.reply_text("An error occurred while fetching the 24h change.")

# Define the command handler for /whales
def whales(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Feature coming soon!")

# Define the command handler for /chart
def chart(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Feature coming soon!")

# Main function to start the bot
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
    dispatcher.add_handler(CommandHandler("chart", chart))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
