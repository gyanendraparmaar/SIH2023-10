import psycopg2

config = {
    "user": "postgres",
    "password": "idkthepassword",
    "host": "0.0.0.0"
}
conn = psycopg2.connect(host=config["host"], user=config["user"], password=config["password"])


def getarticles(page, limit):
    offset = int(page) * int(limit)
    curr = conn.cursor()
    try:
        curr.execute("""SELECT id, link, title, content, created, sentiment, department FROM articles LIMIT %s OFFSET %s;""", (int(limit), int(offset)))
    except psycopg2.ProgrammingError:
        return []
    data = curr.fetchall()
    curr.close()

    return data