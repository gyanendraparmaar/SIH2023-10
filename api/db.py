import psycopg2

config = {
    "user": "postgres",
    "password": "idkthepassword",
    "host": "0.0.0.0",
    "database": "newsDB",
}
conn = psycopg2.connect(**config)


def getarticles(page, limit):
    offset = int(page) * int(limit)
    curr = conn.cursor()
    try:
        curr.execute("""SELECT id, link, title, content, created, sentiment, department FROM articles LIMIT %d OFFSET %d;""", (int(limit), int(offset)))
    except psycopg2.ProgrammingError:
        return []
    data = curr.fetchall()
    curr.close()

    return data