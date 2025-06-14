from flask import Blueprint, render_template, redirect, url_for, jsonify, send_file
from flask_login import login_required, current_user
from models import db, ActivityLog
import os
import json
from io import BytesIO
import pandas as pd
from fpdf import FPDF


dashboard_bp = Blueprint(
    'dashboard',
    __name__,
    template_folder='../../frontend/templates'
)


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


@dashboard_bp.route('/api/data')
@login_required
def api_data():
    """Return sample dashboard data for charts."""
    data_file = os.path.join(os.path.dirname(__file__), '..', 'sample_data.json')
    with open(data_file, 'r') as f:
        data = json.load(f)
    return jsonify(data)


@dashboard_bp.route('/export/<fmt>')
@login_required
def export_data(fmt: str):
    """Export sample dashboard data as Excel or PDF."""
    data_file = os.path.join(os.path.dirname(__file__), '..', 'sample_data.json')
    df = pd.read_json(data_file)
    fmt = fmt.lower()
    if fmt == 'excel':
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return send_file(
            output,
            as_attachment=True,
            download_name='dashboard.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    if fmt == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        col_width = pdf.epw / len(df.columns)
        for col in df.columns:
            pdf.cell(col_width, 10, col, border=1)
        pdf.ln(10)
        for _, row in df.iterrows():
            for item in row:
                pdf.cell(col_width, 10, str(item), border=1)
            pdf.ln(10)
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        return send_file(
            BytesIO(pdf_bytes),
            as_attachment=True,
            download_name='dashboard.pdf',
            mimetype='application/pdf',
        )
    return 'Unsupported format', 400
