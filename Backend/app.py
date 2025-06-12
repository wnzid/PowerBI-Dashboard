from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
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
@app.route('/landing')
def home():
    return render_template('website_landing_page.html')  # Render HTML instead of JSON

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        email = data.get('email') or data.get('Email')
        password = data.get('password') or data.get('Password')
        role = data.get('role') or data.get('Role')
        
        if not email or not password or not role:
            flash('Missing email, password or role', 'error')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute('INSERT INTO users (email, password, role) VALUES (?, ?, ?)', (email, hashed_pw, role))
            conn.commit()
            conn.close()
            session['email'] = email
            session['role'] = role
            if role.lower() == 'manager':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('stakeholder_dashboard'))
        except sqlite3.IntegrityError:
            flash('Email already exists', 'error')
            return redirect(url_for('register'))

    return render_template('registration-page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        email = data.get('email') or data.get('Email')
        password = data.get('password') or data.get('Password')

        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT password, role FROM users WHERE email = ?', (email,))
        row = c.fetchone()
        conn.close()

        if row and check_password_hash(row[0], password):
            session['email'] = email
            session['role'] = row[1]
            if row[1].lower() == 'manager':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('stakeholder_dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session or session.get('role', '').lower() != 'manager':
        return redirect(url_for('login'))
    return render_template('managerial-landing-dashboard.html')

@app.route('/stakeholder')
def stakeholder_dashboard():
    if 'email' not in session or session.get('role', '').lower() != 'stakeholder':
        return redirect(url_for('login'))
    return render_template('stakeholder-landing-dashboard.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Simple password reset placeholder."""
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Please enter your email address.', 'error')
            return redirect(url_for('forgot_password'))

        flash('If an account exists for %s, a reset link has been sent.' % email, 'info')
        return redirect(url_for('login'))

    return render_template('forgot_password.html')


@app.route('/help')
def help_page():
    """Display help and support information."""
    return render_template('help.html')


@app.route('/reports')
def reports():
    """Display available Power BI reports and contact info."""
    return render_template('reports.html')


@app.route('/coming_soon/<page>')
def coming_soon(page):
    """Display placeholder pages for features not yet implemented."""
    title = page.replace('-', ' ').title()
    return render_template('coming_soon.html', page_title=title)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    create_schema()
    app.run(debug=True, port=5001)
