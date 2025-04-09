# RSS_News_Telegram_bot
This is a Python script that monitors multiple RSS feeds and automatically posts new items to a Telegram channel. It supports both general news feeds and keyword-filtered feeds for any pre-determined topics.

## Features

- Fetches RSS feeds and posts new articles to Telegram.
- Supports keyword filtering (e.g., "crypto", "financial", etc.).
- Avoids reposting old articles using timestamp tracking.
- Logging for troubleshooting.
- Customizable for your own feeds or keyword sets.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/telegram-rss-news-bot.git
cd telegram-rss-news-bot
```
### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your bot
Open the script and update the following values:

```bash
BOT_TOKEN = ''  # Your Telegram bot token
CHANNEL_ID =    # Your Telegram channel ID (e.g., -1001234567890)
```

You can find your CHANNEL_ID in thee URL field, using web interface for Telegram.

### 4. Run the bot

```bash
python3 rss_bot.py
```

To keep it running periodically, use a scheduler like cron, systemd, or a cloud automation platform.

### 5. Customisation

Add RSS feeds to ALL_NEWS_FEEDS (always post) or KEYWORD_FILTERED_FEEDS (post only if keywords match).
Modify the KEYWORDS list to suit your use case.


### 6. Logging and timestamps

Logs and timestamps are saved to app.log in the script directory once it runs.
