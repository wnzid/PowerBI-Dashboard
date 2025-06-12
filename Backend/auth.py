from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from models import db, User
from forms import RegistrationForm, LoginForm, ForgotPasswordForm


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register'))
        hashed_pw = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_pw, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        if user.role.lower() == 'manager':
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('dashboard.stakeholder_dashboard'))
    return render_template('registration-page.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.role.lower() == 'manager':
                return redirect(url_for('dashboard.dashboard'))
            return redirect(url_for('dashboard.stakeholder_dashboard'))
        flash('Invalid credentials', 'error')
        return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        flash('If an account exists for %s, a reset link has been sent.' % form.email.data, 'info')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
