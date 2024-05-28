import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Flask-Migrate
import feedparser
from datetime import datetime

app = Flask(__name__)

# Ensure the instance folder exists
if not os.path.exists(app.instance_path):
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

# Update the database URI to point to the instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "news.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Migrate with your Flask app and SQLAlchemy database
migrate = Migrate(app, db)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)

def fetch_feed(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        article = Article(
            title=entry.title,
            link=entry.link,
            published=datetime(*entry.published_parsed[:6]),
            summary=entry.description.split('<img')[0].strip(),
            image_url=entry.description.split('src="')[1].split('"')[0],
        )
        articles.append(article)
    return articles

def store_articles(articles):
    for article in articles:
        if not Article.query.filter_by(link=article.link).first():
            print(f"Storing article: {article.title}")
            db.session.add(article)
    db.session.commit()

@app.route('/')
def index():
    articles = Article.query.order_by(Article.published.desc()).all()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        urls = [
            'https://www.moneycontrol.com/rss/MCtopnews.xml',
            'https://www.moneycontrol.com/rss/marketreports.xml',
            'https://www.moneycontrol.com/rss/business.xml'
        ]
        for url in urls:
            articles = fetch_feed(url)
            store_articles(articles)
    app.run(debug=True)
