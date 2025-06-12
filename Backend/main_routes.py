from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/landing')
def home():
    return render_template('website_landing_page.html')


@main_bp.route('/help')
def help_page():
    """Display help and support information."""
    return render_template('help.html')


@main_bp.route('/reports')
def reports():
    """Display available Power BI reports and contact info."""
    return render_template('reports.html')


@main_bp.route('/coming_soon/<page>')
def coming_soon(page):
    """Display placeholder pages for features not yet implemented."""
    title = page.replace('-', ' ').title()
    return render_template('coming_soon.html', page_title=title)
