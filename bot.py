import json
import logging
from news import get_latest_news
from telegram import Update, ParseMode, Bot
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
    get_latest_trades_for_token,
)
from config import Config

bot = Bot(token=Config.TELEGRAM_TOKEN)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def send_message_to_group(message):
    try:
        bot.send_message(chat_id=Config.TELEGRAM_CHAT_ID, text=message)
        logger.info(f"Sent message to group: {message}")
    except Exception as e:
        logger.error(f"Error sending message to group: {e}")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Glitchbot! Use /help to see available commands.")
    send_message_to_group("Bot has started and is ready to receive commands.")

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

        website_url = token_data.get('profile', {}).get('links', [''])[0]

        context.bot.send_photo(chat_id=update.effective_chat.id, photo=banner_url)

        message = (
            f"\uD83C\uDF10 Token: {token_name} ({token_symbol})\n"
            f"{Config.TOKEN_ADDRESS}\n"
            f"\uD83D\uDCB8 Market Cap: ${market_cap:,.0f}\n"
            f"\uD83D\uDD04 Volume 24h: ${volume_24h:,.0f} 6h: ${volume_6h:,.0f} 1h: ${volume_1h:,.0f} 5m: ${volume_5m:,.0f}\n"
            f"\uD83D\uDCC8 Change 24h: {change_24h:.2f}% 6h: {change_6h:.2f}% 1h: {change_1h:.2f}% 5m: {change_5m:.2f}%\n"
            f"\uD83C\uDFE6 Total Supply: {total_supply} \uD83D\uDCA7 Liquidity: ${liquidity:,.0f}\n"
            f"\uD83C\uDF19 <a href='{token_url}'>Moonshot</a> \uD83C\uDF10 <a href='{website_url}'>Website</a>"
        )

        update.message.reply_text(message, parse_mode=ParseMode.HTML)
        logger.info("Displayed HEADROOM token information.")
    except Exception as e:
        logger.error(f"Error in headroom command: {e}")
        update.message.reply_text("An error occurred while fetching headroom information.")

def news(update: Update, context: CallbackContext) -> None:
    try:
        news_items = get_latest_news()

        if not news_items:
            update.message.reply_text("No news available at the moment.")
            return

        news_message = "\n\n".join(
            [f"\uD83D\uDCF0 <a href='{item['url']}'>{item['title']}</a>\n{item['description']}" for item in news_items[:3]]
        )
        update.message.reply_text(news_message, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error in news command: {e}")
        update.message.reply_text("An error occurred while fetching the latest news.")

def price(update: Update, context: CallbackContext) -> None:
    try:
        current_price = get_current_price()
        message = f"\uD83D\uDCB2 Current Price: ${current_price:.4f}"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in price command: {e}")
        update.message.reply_text("An error occurred while fetching the current price.")

def subscribe(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Subscription feature coming soon!")

def transactions(update: Update, context: CallbackContext) -> None:
    try:
        latest_trades_response = get_latest_trades_for_token()
        
        if isinstance(latest_trades_response, dict):
            latest_trades = latest_trades_response.get('data', [])
        else:
            latest_trades = latest_trades_response

        if not latest_trades:
            update.message.reply_text("No recent transactions found.")
            return

        latest_trade = latest_trades[0]
        block_number = latest_trade.get('blockNumber', 'N/A')
        block_timestamp = latest_trade.get('blockTimestamp', 'N/A')
        pair_id = latest_trade.get('pairId', 'N/A')
        amount0 = latest_trade.get('amount0', 'N/A')
        amount1 = latest_trade.get('amount1', 'N/A')
        price_usd = latest_trade.get('priceUsd', 'N/A')
        volume_usd = latest_trade.get('volumeUsd', 'N/A')
        txn_type = latest_trade.get('type', 'N/A')
        maker = latest_trade.get('maker', 'N/A')
        txn_id = latest_trade.get('txnId', 'N/A')

        message = (
            f"Latest Transaction:\n"
            f"🕒 Block Number: {block_number}\n"
            f"📅 Timestamp: {block_timestamp}\n"
            f"🔄 Pair ID: {pair_id}\n"
            f"💰 Amount0: {amount0}\n"
            f"💰 Amount1: {amount1}\n"
            f"💲 Price (USD): {price_usd}\n"
            f"📊 Volume (USD): {volume_usd}\n"
            f"🔄 Type: {txn_type}\n"
            f"👤 Maker: {maker}\n"
            f"🔗 Transaction ID: {txn_id}\n"
        )

        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in transactions command: {e}")
        update.message.reply_text("An error occurred while fetching transactions information.")

def marketcap(update: Update, context: CallbackContext) -> None:
    try:
        market_cap = get_market_cap()
        message = f"\uD83D\uDCB8 Market Cap: ${market_cap:,.0f}"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in marketcap command: {e}")
        update.message.reply_text("An error occurred while fetching the market cap.")

def volume24h(update: Update, context: CallbackContext) -> None:
    try:
        volume_24h = get_24h_volume()
        message = f"\uD83D\uDD04 Volume 24h: ${volume_24h:,.0f}"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in volume24h command: {e}")
        update.message.reply_text("An error occurred while fetching the 24h volume.")

def change24h(update: Update, context: CallbackContext) -> None:
    try:
        change_24h = get_24h_change()
        message = f"\uD83D\uDCC8 Change 24h: {change_24h:.2f}%"
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in change24h command: {e}")
        update.message.reply_text("An error occurred while fetching the 24h change.")

def whales(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Feature coming soon!")

def chart(update: Update, context: CallbackContext) -> None:
    token_symbol = ' '.join(context.args).upper()
    if not token_symbol:
        update.message.reply_text("Please specify a token symbol. Usage: /chart [token_symbol]")
        return
    update.message.reply_text(f"Token price chart for {token_symbol}. Highs, lows, drama!")

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
    main()
