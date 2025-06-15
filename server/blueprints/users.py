from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from forms import UpdateProfileForm, ChangePasswordForm

users_bp = Blueprint(
    'users',
    __name__,
    template_folder='../../frontend/templates'
)

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form = UpdateProfileForm(obj=current_user)
    if profile_form.validate_on_submit():
        if User.query.filter(User.email == profile_form.email.data, User.id != current_user.id).first():
            flash('Email already in use', 'error')
            return redirect(url_for('users.profile'))
        current_user.email = profile_form.email.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('users.profile'))
    pw_form = ChangePasswordForm()
    return render_template('profile.html', profile_form=profile_form, pw_form=pw_form)

@users_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    pw_form = ChangePasswordForm()
    if pw_form.validate_on_submit():
        if not check_password_hash(current_user.password, pw_form.current_password.data):
            flash('Current password incorrect', 'error')
            return redirect(url_for('users.profile'))
        current_user.password = generate_password_hash(pw_form.new_password.data)
        db.session.commit()
        flash('Password changed successfully', 'success')
        return redirect(url_for('users.profile'))
    flash('Please correct the errors', 'error')
    return redirect(url_for('users.profile'))
