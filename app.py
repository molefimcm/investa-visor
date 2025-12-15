from flask import Flask, render_template, jsonify
from config import SECRET_KEY, DISCLAIMER_TEXT
from db import close_db, init_db

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.teardown_appcontext(close_db)

@app.get("/")
def home():
    return render_template("index.html", disclaimer=DISCLAIMER_TEXT)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/init-db")
def init_database():
    init_db()
    return jsonify({"status": "db initialized"})

if __name__ == "__main__":
    app.run(debug=True)
