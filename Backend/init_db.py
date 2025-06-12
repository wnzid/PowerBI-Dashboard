import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
"""

def init_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(SCHEMA)
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}.")

if __name__ == "__main__":
    init_db()
