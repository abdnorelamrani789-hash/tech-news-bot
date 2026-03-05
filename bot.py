# bot.py
import os
import json
import feedparser
import requests

# ==========================
# جلب التوكن و Chat ID من GitHub Secrets
# ==========================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# ==========================
# لائحة RSS feeds
# ==========================
FEEDS_FILE = "feeds.json"
POSTED_FILE = "posted.json"

# تحميل الأخبار المنشورة لتجنب التكرار
try:
    with open(POSTED_FILE, "r") as f:
        posted = json.load(f)
except:
    posted = []

# قراءة RSS feeds
with open(FEEDS_FILE, "r") as f:
    feeds = json.load(f)

# كلمات مفتاحية بسيطة لتصنيف الأخبار
CATEGORIES = {
    "AI": ["AI", "Artificial Intelligence", "ChatGPT", "machine learning", "deep learning"],
    "Cybersecurity": ["security", "cyber", "hacking", "malware", "vulnerability"],
    "Cloud": ["cloud", "AWS", "Azure", "GCP", "serverless"],
    "Programming": ["Python", "JavaScript", "Java", "programming", "code"]
}

def classify(title, summary):
    title_lower = title.lower()
    summary_lower = summary.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw.lower() in title_lower or kw.lower() in summary_lower:
                return cat
    return "Other"

# ==========================
# معالجة كل feed
# ==========================
for feed_url in feeds:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        news_id = entry.link
        if news_id in posted:
            continue  # تخطي الأخبار اللي سبق نشرها

        title = entry.title
        summary = entry.summary[:300] + "..."  # ملخص قصير
        category = classify(title, summary)

        # توليد الرسالة
        message = f"📢 [{category}] {title}\n{summary}\n{entry.link}"

        # إرسال لتليجرام
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": message})
        if response.status_code == 200:
            print(f"تم نشر: {title}")
        else:
            print(f"خطأ في النشر: {title} - {response.text}")

        # تخزين الخبر المنشور
        posted.append(news_id)

# تحديث ملف posted.json
with open(POSTED_FILE, "w") as f:
    json.dump(posted, f)
