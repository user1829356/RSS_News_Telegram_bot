import feedparser
import datetime
import os
import json
import logging
import requests
import time

# These feeds will post every time a news comes out
ALL_NEWS_FEEDS = {
    "NYT": 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    "BBC": 'http://feeds.bbci.co.uk/news/rss.xml',
}
#These feeds will post in Telegram channel only when there is a match for the keywords
KEYWORD_FILTERED_FEEDS = {
    #"NYT": 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    #"BBC": 'http://feeds.bbci.co.uk/news/rss.xml',
}

KEYWORDS = ['financial', 'stock', 'crypto']

TIMESTAMPS_FILE = os.path.dirname(os.path.realpath(__file__))+'/timestamps.json'
BOT_TOKEN = ''  # Replace with your Telegram Bot Token
CHANNEL_ID =   # Replace with your channel's username or channel ID, for example: -10034107254734

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename=os.path.dirname(os.path.realpath(__file__))+"/app.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

def send_to_telegram(title, link, description):
    message = f"**{title}**\n{link}\n\n{description}"
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHANNEL_ID, 'text': message, 'parse_mode': 'Markdown'}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        logging.info(f"Sent to Telegram: {title}")
    else:
        logging.error(f"Failed to send to Telegram: {response.text}")

def load_timestamps():
    if os.path.exists(TIMESTAMPS_FILE):
        with open(TIMESTAMPS_FILE, 'r') as f:
            data = json.load(f)
            logging.debug("Loaded timestamps.")
            return {key: datetime.datetime.fromisoformat(value) for key, value in data.items()}
    logging.debug("No timestamps file found. Starting fresh.")
    return {}

def save_timestamps(timestamps):
    with open(TIMESTAMPS_FILE, 'w') as f:
        json_data = {key: value.isoformat() for key, value in timestamps.items()}
        json.dump(json_data, f, indent=4)
    logging.debug("Saved timestamps.")

def get_news_from_feed(feed_url, feed_name, timestamps, filter_by_keywords=False):
    logging.info(f"Processing feed: {feed_name}")
    last_time_checked = timestamps.get(feed_name, datetime.datetime.now() - datetime.timedelta(days=1))
    feed = feedparser.parse(feed_url)
    relevant_news = []

    if not feed.entries:
        logging.debug(f"No new entries found for {feed_name}.")
        return [], last_time_checked

    latest_timestamp = last_time_checked
    for entry in feed.entries:
        published_time = datetime.datetime(*entry.published_parsed[:6])
        if published_time > last_time_checked:
            if filter_by_keywords and not any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.description.lower() for keyword in KEYWORDS):
                continue  # Skip this news item if it does not match any keyword
            relevant_news.append(entry)
            if published_time > latest_timestamp:
                latest_timestamp = published_time

    if relevant_news:
        logging.info(f"Found {len(relevant_news)} new relevant news items in {feed_name}.")
    else:
        logging.debug(f"No new relevant news found in {feed_name} since last check.")

    return relevant_news, latest_timestamp

def main():
    logging.info("Script started")
    timestamps = load_timestamps()

    # Process all news feeds
    for feed_name, feed_url in ALL_NEWS_FEEDS.items():
        news, latest_timestamp = get_news_from_feed(feed_url, feed_name, timestamps, filter_by_keywords=False)
        for item in news:
            send_to_telegram(item.title, item.link, item.description)
            time.sleep(5)
        timestamps[feed_name] = latest_timestamp

    # Process keyword-filtered news feeds
    for feed_name, feed_url in KEYWORD_FILTERED_FEEDS.items():
        news, latest_timestamp = get_news_from_feed(feed_url, feed_name, timestamps, filter_by_keywords=True)
        for item in news:
            send_to_telegram(item.title, item.link, item.description)
            time.sleep(5)
        timestamps[feed_name] = latest_timestamp

    save_timestamps(timestamps)
    logging.info("Script finished successfully")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
