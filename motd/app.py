from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import datetime

app = Flask(__name__)

ADMIN_PASSWORD = "admin123"  # Change this for security

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_word_of_the_day():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM words")
    total_words = cursor.fetchone()[0]

    if total_words == 0:
        return {"word": "No words found", "meaning": "Please add words to the database."}

    day_index = datetime.datetime.now().day % total_words
    cursor.execute("SELECT word, meaning FROM words LIMIT 1 OFFSET ?", (day_index,))
    word = cursor.fetchone()
    conn.close()

    return {"word": word["word"], "meaning": word["meaning"]}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/word")
def api_word():
    return jsonify(get_word_of_the_day())

# Admin Panel Route
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form["password"]
        if password != ADMIN_PASSWORD:
            return "Unauthorized", 401
    
    conn = get_db_connection()
    words = conn.execute("SELECT * FROM words").fetchall()
    conn.close()
    return render_template("admin.html", words=words)

# Add Word
@app.route("/add_word", methods=["POST"])
def add_word():
    word = request.form["word"]
    meaning = request.form["meaning"]
    
    conn = get_db_connection()
    conn.execute("INSERT INTO words (word, meaning) VALUES (?, ?)", (word, meaning))
    conn.commit()
    conn.close()
    
    return redirect(url_for("admin"))

# Delete Word
@app.route("/delete_word/<int:id>", methods=["POST"])
def delete_word(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM words WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)
