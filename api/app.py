from flask import Flask
from flask import render_template, request

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
    

if __name__ == "__main__":
    app.run(debug=True, port=9999)