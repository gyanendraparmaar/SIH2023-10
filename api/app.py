from flask import Flask
from flask import render_template, request
from db import getarticles

app = Flask(__name__)
routes = ["/ping"]

@app.route("/")
def home():
    return render_template("home.html", routes=routes)

@app.route("/ping")
def ping():
    return {"status": "success", "data": "pong"}

@app.route("/articles", methods=["POST"])
def getArticles():
    page = request.args.get("page")
    limit = request.args.get("limit")
    if page == None:
        page = "0"
    if limit == None:
        limit = "100"
    if not page.isnumeric():
        return {"status": "fail", "data": "invalid request - page"}
    if not limit.isnumeric():
        return {"status": "fail", "data": "invalid request - limit"}
    data = getarticles(page, limit)
    if data == []:
        return {"status": "fail", "data": "DBError"}
    return {"status": "success", "data": data}


if __name__ == "__main__":
    app.run(debug=True, port=8001, host="0.0.0.0")