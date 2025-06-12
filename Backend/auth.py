from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        email = data.get('email') or data.get('Email')
        password = data.get('password') or data.get('Password')
        role = data.get('role') or data.get('Role')

        if not email or not password or not role:
            flash('Missing email, password or role', 'error')
            return redirect(url_for('auth.register'))

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
                return redirect(url_for('dashboard.dashboard'))
            else:
                return redirect(url_for('dashboard.stakeholder_dashboard'))
        except sqlite3.IntegrityError:
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register'))

    return render_template('registration-page.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('dashboard.dashboard'))
            else:
                return redirect(url_for('dashboard.stakeholder_dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Simple password reset placeholder."""
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Please enter your email address.', 'error')
            return redirect(url_for('auth.forgot_password'))

        flash('If an account exists for %s, a reset link has been sent.' % email, 'info')
        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))
