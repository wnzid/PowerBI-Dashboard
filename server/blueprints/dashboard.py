from flask import Blueprint, render_template, redirect, url_for, jsonify, send_file, flash, request
from flask_login import login_required, current_user
from models import db, ActivityLog, ImportedData, CSVFile
from forms import CSVUploadForm
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
    data_file = os.path.join(os.path.dirname(__file__), 'sample_data.json')
    with open(data_file, 'r') as f:
        data = json.load(f)
    return jsonify(data)


@dashboard_bp.route('/export/<fmt>')
@login_required
def export_data(fmt: str):
    """Export sample dashboard data as Excel or PDF."""
    data_file = os.path.join(os.path.dirname(__file__), 'sample_data.json')
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


@dashboard_bp.route('/admin/import-data', methods=['GET', 'POST'])
@login_required
def import_data():
    """Admin upload of CSV or Excel files"""
    if current_user.role.name.lower() != 'admin':
        return redirect(url_for('auth.login'))
    form = CSVUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        ext = os.path.splitext(file.filename)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(file)
        elif ext in ('.xlsx', '.xls'):
            df = pd.read_excel(file)
        else:
            flash('Unsupported file format', 'error')
            return redirect(url_for('dashboard.import_data'))
        csv_file = CSVFile(filename=file.filename, uploaded_by=current_user)
        db.session.add(csv_file)
        db.session.flush()
        for _, row in df.iterrows():
            db.session.add(
                ImportedData(
                    data=row.to_dict(),
                    uploaded_by=current_user,
                    csv_file=csv_file,
                )
            )
        db.session.commit()
        flash('Data imported', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('import_data.html', form=form)


@dashboard_bp.route('/api/imported')
@login_required
def api_imported():
    """Return recently imported data for managers."""
    if current_user.role.name.lower() != 'manager':
        return jsonify([])
    records = ImportedData.query.order_by(ImportedData.timestamp.desc()).all()
    payload = [
        {
            'id': r.id,
            'data': r.data,
            'approved': r.approved,
            'file_id': r.csv_file_id,
            'file_status': r.csv_file.status if r.csv_file else None,
            'file_active': r.csv_file.active if r.csv_file else None,
            'timestamp': r.timestamp.isoformat()
        }
        for r in records
    ]
    return jsonify(payload)


@dashboard_bp.route('/approve/<int:record_id>', methods=['POST'])
@login_required
def approve_record(record_id: int):
    if current_user.role.name.lower() != 'manager':
        return 'Forbidden', 403
    rec = db.session.get(ImportedData, record_id)
    if rec:
        rec.approved = True
        db.session.commit()
    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/api/published')
@login_required
def api_published():
    if current_user.role.name.lower() != 'stakeholder':
        return jsonify([])
    records = (
        ImportedData.query.join(CSVFile)
        .filter(
            ImportedData.approved.is_(True),
            CSVFile.status == 'approved',
            CSVFile.active.is_(True),
        )
        .all()
    )
    payload = [r.data for r in records]
    return jsonify(payload)


# ----- Manager specific pages -----

@dashboard_bp.route('/report/<report_name>')
@login_required
def report_detail(report_name: str):
    if current_user.role.name.lower() != 'manager':
        return redirect(url_for('auth.login'))
    title = report_name.replace('-', ' ').title()
    return render_template('manager-report.html', report_name=report_name, title=title)


@dashboard_bp.route('/manager/create-dashboard')
@login_required
def create_dashboard():
    if current_user.role.name.lower() != 'manager':
        return redirect(url_for('auth.login'))
    return render_template('create_dashboard.html')


@dashboard_bp.route('/manager/download-data')
@login_required
def download_data_page():
    if current_user.role.name.lower() != 'manager':
        return redirect(url_for('auth.login'))
    return render_template('download_data.html')


@dashboard_bp.route('/manager/settings')
@login_required
def settings_page():
    if current_user.role.name.lower() != 'manager':
        return redirect(url_for('auth.login'))
    return render_template('settings.html')


# ---- Admin CSV file management ----

@dashboard_bp.route('/admin/csv-files')
@login_required
def list_csv_files():
    if current_user.role.name.lower() != 'admin':
        return redirect(url_for('auth.login'))
    files = CSVFile.query.order_by(CSVFile.timestamp.desc()).all()
    return render_template('admin_csv_files.html', files=files)


@dashboard_bp.route('/admin/csv-files/hide/<int:file_id>', methods=['POST'])
@login_required
def toggle_csv_file(file_id: int):
    if current_user.role.name.lower() != 'admin':
        return redirect(url_for('auth.login'))
    f = db.session.get(CSVFile, file_id)
    if f:
        f.active = not f.active
        db.session.commit()
    return redirect(url_for('dashboard.list_csv_files'))


@dashboard_bp.route('/admin/csv-files/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_csv_file(file_id: int):
    if current_user.role.name.lower() != 'admin':
        return redirect(url_for('auth.login'))
    f = db.session.get(CSVFile, file_id)
    if f:
        ImportedData.query.filter_by(csv_file_id=file_id).delete()
        db.session.delete(f)
        db.session.commit()
    return redirect(url_for('dashboard.list_csv_files'))


# ---- Manager CSV approval ----

@dashboard_bp.route('/manager/csv-files')
@login_required
def manager_csv_files():
    if current_user.role.name.lower() != 'manager':
        return redirect(url_for('auth.login'))
    files = CSVFile.query.filter_by(status='pending').order_by(CSVFile.timestamp.desc()).all()
    return render_template('manager_csv_files.html', files=files)


@dashboard_bp.route('/manager/csv-files/approve/<int:file_id>', methods=['POST'])
@login_required
def approve_csv_file(file_id: int):
    if current_user.role.name.lower() != 'manager':
        return '', 403
    f = db.session.get(CSVFile, file_id)
    if f:
        f.status = 'approved'
        for row in f.rows:
            row.approved = True
        db.session.commit()
    return '', 204


@dashboard_bp.route('/manager/csv-files/decline/<int:file_id>', methods=['POST'])
@login_required
def decline_csv_file(file_id: int):
    if current_user.role.name.lower() != 'manager':
        return '', 403
    f = db.session.get(CSVFile, file_id)
    if f:
        f.status = 'declined'
        for row in f.rows:
            row.approved = False
        db.session.commit()
    return '', 204
