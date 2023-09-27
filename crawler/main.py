from crawl import Crawl
import psycopg2
import datetime

import pika
import json

import random

class App:
    def __init__(self):
        self.mydb = psycopg2.connect(
            host = "localhost",
            user = "postgres",
            password = "idkthepassword",
        )
        self.cursor = self.mydb.cursor()
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue = "toCrawl")

    def insertArticle(self, article):
        self.cursor.execute("INSERT INTO articles (link, title, content, created, sentiment, department, lang) VALUES (%s, %s, %s, %s, %s, %s, %s)", ( article["url"], article["headline"], article["articleBody"], datetime.datetime.now().isoformat(), article["sentiment"], article["department"], article["inLanguage"] ))

    def callback(self, ch, method, properties, body):
        req = json.loads(body)
        crawler = Crawl(lang = req['lang'], provider = req['provider'])
        
        for url in req["urls"]:
            article = crawler.getNews(url)
            
            if article:
                # Do sentiment analysis + department prediction
                article["sentiment"] = round(random.random(), 3)
                article["department"] = "noone"

                self.insertArticle(article)

        self.mydb.commit()

    def listen(self):
        self.channel.basic_consume(queue = "toCrawl", on_message_callback = self.callback, auto_ack = True)
        self.channel.start_consuming()

if __name__ == "__main__":
    app = App()
    app.listen()