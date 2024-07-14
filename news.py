import requests
import logging
from config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_latest_news():
    try:
        # Using the /everything endpoint to fetch news related to Solana
        url = f"https://newsapi.org/v2/everything?q=memecoin&apiKey={Config.NEWS_API_KEY}&pageSize=3"
        logger.debug(f"Fetching news from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        logger.debug(f"Received news data: {news_data}")
        articles = news_data.get('articles', [])
        if not articles:
            logger.debug("No articles found in news data.")
        news_items = [
            {
                'title': article['title'],
                'description': article['description'],
                'url': article['url']
            } for article in articles
        ]
        return news_items
    except Exception as e:
        logger.error(f"Error fetching latest news: {e}")
        return []
