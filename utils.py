import requests
import logging
from config import NEWS_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levellevel)%s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_latest_news():
    try:
        url = f"https://newsapi.org/v2/everything?q=solana&apiKey={NEWS_TOKEN}"
        logger.debug(f"Fetching news with URL: {url}")
        response = requests.get(url)
        logger.debug(f"Response status code: {response.status_code}")
        if response.status_code != 200:
            logger.error("Error fetching news.")
            return []

        news_data = response.json()
        articles = news_data.get('articles', [])
        news_items = []
        for article in articles[:5]:
            news_item = {
                'title': article['title'],
                'description': article['description'],
                'url': article['url']
            }
            news_items.append(news_item)
        return news_items
    except Exception as e:
        logger.error(f"Error fetching latest news: {e}")
        return []
