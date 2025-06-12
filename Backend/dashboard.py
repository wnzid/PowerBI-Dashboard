from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import db, ActivityLog


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name.lower() != 'manager':
        return redirect(url_for('auth.login'))
    db.session.add(ActivityLog(user_id=current_user.id, activity_type='view_manager_dashboard'))
    db.session.commit()
    return render_template('managerial-landing-dashboard.html')


@dashboard_bp.route('/stakeholder')
@login_required
def stakeholder_dashboard():
    if current_user.role.name.lower() != 'stakeholder':
        return redirect(url_for('auth.login'))
    db.session.add(ActivityLog(user_id=current_user.id, activity_type='view_stakeholder_dashboard'))
    db.session.commit()
    return render_template('stakeholder-landing-dashboard.html')
