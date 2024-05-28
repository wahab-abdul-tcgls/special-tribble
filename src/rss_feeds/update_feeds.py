from app import fetch_feed, store_articles, db

db.create_all()
urls = [
    'https://www.moneycontrol.com/rss/MCtopnews.xml',
    'https://www.moneycontrol.com/rss/marketreports.xml',
    'https://www.moneycontrol.com/rss/business.xml'
]
for url in urls:
    articles = fetch_feed(url)
    store_articles(articles)
