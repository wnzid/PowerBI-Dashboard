import os
import sqlite3

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'Backend', 'users.db')

# SQL schema for the users table
SCHEMA = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
'''

def get_connection():
    """Return a new database connection."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize the database using the schema."""
    conn = get_connection()
    conn.execute(SCHEMA)
    conn.commit()
    conn.close()
