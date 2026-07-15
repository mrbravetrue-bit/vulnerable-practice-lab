"""
app.py
A deliberately vulnerable practice lab for learning web application
security — the same educational pattern as tools like DVWA/WebGoat/Juice
Shop, built from scratch to show the underlying mechanics.

⚠️ IMPORTANT — READ BEFORE RUNNING
  - This app contains INTENTIONAL vulnerabilities (SQL injection, stored
    XSS) in its "vulnerable" mode routes. That is the point — it's a lab.
  - Run it ONLY on localhost, on a machine you control, disconnected from
    any network you don't fully trust. NEVER deploy this to a public
    server or expose it to the internet.
  - Each lab also has a "secure" mode showing the fixed version, so you
    can diff the two and see exactly what changed.

Usage:
    pip install -r requirements.txt
    python3 app.py
    # then open http://127.0.0.1:5000
"""
import sqlite3
from flask import Flask, request, render_template, abort
import database

app = Flask(__name__)

VALID_MODES = {"vulnerable", "secure"}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login/<mode>", methods=["GET", "POST"])
def login(mode):
    if mode not in VALID_MODES:
        abort(404)

    result = None
    query_used = None
    attempted = request.method == "POST"

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = database.get_connection()

        if mode == "vulnerable":
            # ⚠️ INTENTIONALLY VULNERABLE: raw string concatenation into SQL.
            # Try username=admin, password=' OR '1'='1
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            query_used = query
            try:
                result = conn.execute(query).fetchone()
            except sqlite3.Error as e:
                query_used += f"\n-- SQL error: {e}"
                result = None
        else:
            # ✅ SECURE: parameterized query — user input is never
            # concatenated into the SQL string, so it can't change the
            # query's structure no matter what characters it contains.
            result = conn.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password),
            ).fetchone()

        conn.close()

    return render_template("login.html", mode=mode, result=result, query_used=query_used, attempted=attempted)


@app.route("/guestbook/<mode>", methods=["GET", "POST"])
def guestbook(mode):
    if mode not in VALID_MODES:
        abort(404)

    conn = database.get_connection()

    if request.method == "POST":
        author = request.form.get("author", "anonymous") or "anonymous"
        message = request.form.get("message", "")
        conn.execute(
            "INSERT INTO guestbook (author, message) VALUES (?, ?)", (author, message)
        )
        conn.commit()

    entries = conn.execute("SELECT * FROM guestbook ORDER BY id DESC").fetchall()
    conn.close()

    # Note: the vulnerable/secure difference for this lab lives in the
    # template (guestbook.html) — vulnerable mode renders `entry.message`
    # with the `|safe` filter (disabling auto-escaping), secure mode does not.
    return render_template("guestbook.html", mode=mode, entries=entries)


if __name__ == "__main__":
    database.init_db()
    print("[*] Lab database initialized (reset to seed data).")
    print("[*] Starting on http://127.0.0.1:5000 — Ctrl+C to stop.")
    app.run(debug=True, host="127.0.0.1", port=5000)
