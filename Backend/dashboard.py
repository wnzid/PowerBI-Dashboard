from flask import Blueprint, render_template, session, redirect, url_for


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():
    if 'email' not in session or session.get('role', '').lower() != 'manager':
        return redirect(url_for('auth.login'))
    return render_template('managerial-landing-dashboard.html')


@dashboard_bp.route('/stakeholder')
def stakeholder_dashboard():
    if 'email' not in session or session.get('role', '').lower() != 'stakeholder':
        return redirect(url_for('auth.login'))
    return render_template('stakeholder-landing-dashboard.html')
