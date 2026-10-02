import os

import pymysql
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "version": "2.0"
    })


@app.route("/clients")
def clients():
    connection = get_db_connection()

    cursor = connection.cursor()
    cursor.execute("SELECT id, name FROM clients")
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify([
        {"id": row[0], "name": row[1]}
        for row in results
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)