import json
import feedparser
import requests

BOT_TOKEN = "8642429277:AAFRm12sxHrBKIetg54IOyyW4TEcng3PEV8"
CHAT_ID = "@YourChannelName"

# تحميل الأخبار المنشورة
try:
    with open("posted.json", "r") as f:
        posted = json.load(f)
except:
    posted = []

# قراءة RSS feeds
with open("feeds.json", "r") as f:
    feeds = json.load(f)

for feed_url in feeds:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        news_id = entry.link
        if news_id in posted:
            continue

        title = entry.title
        summary = entry.summary[:300] + "..."
        message = f"📢 {title}\n{summary}\n{entry.link}"

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})

        posted.append(news_id)

with open("posted.json", "w") as f:
    json.dump(posted, f)
