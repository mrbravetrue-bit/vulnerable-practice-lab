"""
database.py
Sets up an in-memory-per-run SQLite database for the lab: a `users` table
(for the SQL injection lab) and a `guestbook` table (for the XSS lab).
Resets to known seed data every time the app starts, so the lab is always
in a clean, predictable state.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "lab.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(
        """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS guestbook;

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        );

        CREATE TABLE guestbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """
    )
    # Seed data — deliberately simple/demo credentials, this is a local lab only.
    conn.executemany(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        [
            ("alice", "alicepass123", "user"),
            ("admin", "sup3rSecretAdminPW!", "admin"),
        ],
    )
    conn.executemany(
        "INSERT INTO guestbook (author, message) VALUES (?, ?)",
        [
            ("visitor1", "Great site, learned a lot here!"),
            ("visitor2", "Looking forward to more content."),
        ],
    )
    conn.commit()
    conn.close()
