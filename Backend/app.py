import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from cryptography.fernet import Fernet
import sqlite3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key().decode()
    print(f"Generated Fernet key: {FERNET_KEY} (set this as FERNET_KEY in your .env file)")
cipher = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL)""")
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__,
            static_folder="static",
            static_url_path="/static",
            template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")

def encrypt_pw(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

def decrypt_pw(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()

@app.route("/managerial")
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("managerial-landing-dashboard.html")

@app.route("/stakeholder")
def stakeholder_dashboard():
    return render_template("stakeholder-landing-dashboard.html")

@app.route("/")
def landing():
    return render_template("website_landing_page.html")

@app.route("/coming-soon/<page>")
def coming_soon(page):
    title = page.replace("-", " ").title()
    return render_template("coming_soon.html", page_title=title)

@app.route("/forgot-password")
def forgot_password():
    return render_template("coming_soon.html", page_title="Forgot Password")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("Email")
        password = request.form.get("Password")
        role = request.form.get("Role")  # Make sure your registration form provides this

        if not password or len(password) < 12:
            flash("Password must be at least 12 characters long.", "error")
            return redirect(url_for("register"))

        encrypted_pw = encrypt_pw(password)

        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                      (email, encrypted_pw, role))
            conn.commit()
            conn.close()

            session['email'] = email
            session['role'] = role

            if role == "Manager":
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("stakeholder_dashboard"))

        except sqlite3.IntegrityError:
            conn.close()
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT role FROM users WHERE email = ?", (email,))
            result = c.fetchone()
            conn.close()

            if result:
                existing_role = result[0]
                message = f"This email is already registered as {existing_role}"
            else:
                message = "This email is already registered"

            flash(message, "error")
            return redirect(url_for("register"))

    return render_template("registration-page.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT password, role FROM users WHERE email = ?", (email,))
        result = c.fetchone()
        conn.close()

        if result:
            stored_password, role = result
            login_ok = False
            try:
                decrypted = decrypt_pw(stored_password)
                if decrypted == password:
                    login_ok = True
            except Exception:
                from werkzeug.security import check_password_hash
                if check_password_hash(stored_password, password):
                    login_ok = True

            if login_ok:
                session['email'] = email
                session['role'] = role

                if role == "Manager":
                    return redirect(url_for("dashboard"))
                else:
                    return redirect(url_for("stakeholder_dashboard"))
            else:
                flash("Incorrect password", "error")
                return redirect(url_for("login"))
        else:
            flash("User not found", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))

@app.route("/api/data")
def api_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM users", conn)
        conn.close()
        df = df.fillna(0)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
