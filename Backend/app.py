from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection, init_db
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

def create_schema():
    """Ensure the users table exists with the expected fields."""
    conn = get_connection()
    conn.execute(
        '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )'''
    )
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('website_landing_page.html')  # Render HTML instead of JSON

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or request.form
    email = data.get('email') or data.get('Email')
    password = data.get('password') or data.get('Password')
    role = data.get('role') or data.get('Role')
    
    if not email or not password or not role:
        return jsonify({'error': 'Missing email, password or role'}), 400

    hashed_pw = generate_password_hash(password)
    
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO users (email, password, role) VALUES (?, ?, ?)', (email, hashed_pw, role))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or request.form
    email = data.get('email') or data.get('Email')
    password = data.get('password') or data.get('Password')

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE email = ?', (email,))
    row = c.fetchone()
    conn.close()

    if row and check_password_hash(row[0], password):
        session['username'] = email  # Store email in session as username
        return redirect(url_for('dashboard'))
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html', username=session['username'])

if __name__ == '__main__':
    init_db()
    create_schema()
    app.run(debug=True, port=5001)
