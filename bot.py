import feedparser
import requests
import time

# ----------- إعدادات البوت -----------
TELEGRAM_BOT_TOKEN = "8642429277:AAFRm12sxHrBKIetg54IOyyW4TEcng3PEV8"
TELEGRAM_CHAT_ID = -1003814843921  # Chat ID الرقمي للقناة
DELAY_BETWEEN_MESSAGES = 2  # ثواني

# ----------- قائمة المواقع (RSS) -----------
RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://news.ycombinator.com/rss",
    # تقدر تزيد أي موقع RSS مجاني
]

# ----------- وظيفة إرسال رسالة للبوت -----------
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    response = requests.post(url, data=payload)
    result = response.json()
    
    if result.get("ok"):
        print(f"تم نشر: {text}")
    else:
        print(f"خطأ في النشر: {text} - {result}")

# ----------- وظيفة جلب الأخبار -----------
def fetch_news():
    news_items = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # آخر 5 أخبار من كل feed
            news_items.append({
                "title": entry.title,
                "link": entry.link
            })
    return news_items

# ----------- الوظيفة الرئيسية -----------
def main():
    news_list = fetch_news()
    for news in news_list:
        message_text = f"{news['title']}\n{news['link']}"
        send_telegram_message(message_text)
        time.sleep(DELAY_BETWEEN_MESSAGES)  # تأخير بين كل رسالة

if __name__ == "__main__":
    main()
