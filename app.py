from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random

app = Flask(__name__)
DATABASE = "shortener.db"

# ------------------ Database Setup ------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

# ------------------ Generate Short Code ------------------
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ------------------ Home Page ------------------
@app.route('/')
def home():
    return render_template("index.html")

# ------------------ Shorten URL ------------------
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    short_code = generate_short_code()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
                   (original_url, short_code))
    conn.commit()
    conn.close()

    short_url = request.host_url + short_code
    return render_template("index.html", short_url=short_url)

# ------------------ Redirect ------------------
@app.route('/<short_code>')
def redirect_to_original(short_code):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_code=?",
                   (short_code,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    return "URL not found", 404

# ------------------ Run ------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True , port=5001)