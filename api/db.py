import mysql.connector

config = {
    "user": "admin",
    "password": "idkthepassword",
    "host": "127.0.0.1",
}
conn = mysql.connector.connect(**config)


def getarticles(page):
    query = """SELECT """