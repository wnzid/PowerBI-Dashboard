from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer, BadSignature
from flask_mail import Message
from models import db, User, Role, ActivityLog
from forms import (
    RegistrationForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    UpdateProfileForm,
    ChangePasswordForm,
)
from extensions import mail


auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='../../frontend/templates'
)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Exclude the Admin role from the registration choices
    form.role.choices = [
        (r.id, r.name) for r in Role.query.filter(Role.name != "Admin")
    ]
    if form.validate_on_submit():
        selected_role = db.session.get(Role, form.role.data)
        if selected_role and selected_role.name.lower() == "admin":
            flash("Admin registration is not allowed", "error")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register'))
        hashed_pw = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_pw, role_id=form.role.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        db.session.add(ActivityLog(user_id=user.id, activity_type='login_success'))
        db.session.commit()
        if user.role.name.lower() == 'manager':
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
            flash('Logged in successfully', 'success')
            db.session.add(ActivityLog(user_id=user.id, activity_type='login_success'))
            db.session.commit()
            if user.role.name.lower() == 'manager':
                return redirect(url_for('dashboard.dashboard'))
            if user.role.name.lower() == 'admin':
                return redirect(url_for('admin.index'))
            return redirect(url_for('dashboard.stakeholder_dashboard'))
        db.session.add(ActivityLog(user_id=user.id if user else None, activity_type='login_failed'))
        db.session.commit()
        flash('Invalid credentials', 'error')
        return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = serializer.dumps(user.id)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message('Password Reset', recipients=[user.email])
            msg.body = f'Click the link to reset your password: {reset_url}'
            mail.send(msg)
        flash('If an account exists for %s, a reset link has been sent.' % form.email.data, 'info')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token: str):
    form = ResetPasswordForm()
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(token, max_age=3600)
    except BadSignature:
        flash('Invalid or expired token', 'error')
        return redirect(url_for('auth.login'))
    user = db.session.get(User, user_id)
    if not user:
        flash('Invalid token', 'error')
        return redirect(url_for('auth.login'))
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Password reset successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form, token=token)


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form = UpdateProfileForm(obj=current_user)
    if profile_form.validate_on_submit():
        if User.query.filter(User.email == profile_form.email.data, User.id != current_user.id).first():
            flash('Email already in use', 'error')
            return redirect(url_for('auth.profile'))
        current_user.email = profile_form.email.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('auth.profile'))
    pw_form = ChangePasswordForm()
    return render_template('profile.html', profile_form=profile_form, pw_form=pw_form)


@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    profile_form = UpdateProfileForm()  # not used
    pw_form = ChangePasswordForm()
    if pw_form.validate_on_submit():
        if not check_password_hash(current_user.password, pw_form.current_password.data):
            flash('Current password incorrect', 'error')
            return redirect(url_for('auth.profile'))
        current_user.password = generate_password_hash(pw_form.new_password.data)
        db.session.commit()
        flash('Password changed successfully', 'success')
        return redirect(url_for('auth.profile'))
    flash('Please correct the errors', 'error')
    return redirect(url_for('auth.profile'))


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('main.home'))
