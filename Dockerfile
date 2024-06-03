FROM python:3.11
COPY . /app
WORKDIR /app/src/rss_feeds
RUN pip install -r requirements.txt
CMD python app.py


