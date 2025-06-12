from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection, init_db
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session

def create_schema():
    """Ensure the users table exists."""
    conn = get_connection()
    conn.execute(
        '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )'''
    )
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({'message': 'API is running'}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    hashed_pw = generate_password_hash(password)
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row and check_password_hash(row[0], password):
        session['username'] = username
        return redirect(url_for('dashboard'))  # Redirect to dashboard
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    # Initialize both the shared database and the local schema
    init_db()
    create_schema()
    app.run(debug=True, port=5001)
