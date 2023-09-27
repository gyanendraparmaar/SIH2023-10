from crawl import Crawl
import psycopg2
import datetime

import pika
import json

mydb = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    password = "idkthepassword",
    database = "newsDB"
)

class App:
    def __init__(self):
        self.cursor = mydb.cursor()
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue = "toCrawl")

    def insertArticle(self, article):
        self.cursor.execute(f'INSERT INTO articles (link, title, content, created, sentiment, department, language) VALUES ({article["url"]}, {article["headline"]}, {article["articleBody"]}, {datetime.datetime.now().isoformat()}, {article["sentiment"]}, {article["department"]}, {article["inLanguage"]})')

    def callback(self, ch, method, properties, body):
        req = json.loads(body)
        crawler = Crawl(lang = req['lang'], provider = req['provider'])
        
        for url in req["urls"]:
            article = crawler.getNews(url)

            # Do sentiment analysis + department prediction

            self.insertArticle(article)

    def listen(self):
        self.channel.basic_consume(queue = "toCrawl", on_message_callback = self.callback, auto_ack = True)
        self.channel.start_consuming()

if __name__ == "__main__":
    app = App()
    app.listen()