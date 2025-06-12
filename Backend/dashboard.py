from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.lower() != 'manager':
        return redirect(url_for('auth.login'))
    return render_template('managerial-landing-dashboard.html')


@dashboard_bp.route('/stakeholder')
@login_required
def stakeholder_dashboard():
    if current_user.role.lower() != 'stakeholder':
        return redirect(url_for('auth.login'))
    return render_template('stakeholder-landing-dashboard.html')
