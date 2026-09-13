<div align="center">
  <img src="frontend/static/Assets/logo.png" width="96" alt="Analytics Institute portal logo" />

# Power BI Dashboard Portal

**Role-aware analytics delivery for managers, stakeholders, and administrators.**

`Flask` · `SQLAlchemy` · `Power BI` · `Pandas` · `Bootstrap`

</div>

This Flask application hosts embedded Power BI dashboards for the Analytics Institute of Australia and adds the workflows around them: account access, role-based navigation, profile management, data imports, approvals, exports, and administrative oversight.

## Capabilities

- Manager and Stakeholder dashboard experiences
- Administrator-only user and role management
- Registration, sign-in, profile editing, password change, and email recovery
- CSRF protection, session management, and production HTTPS redirect
- Embedded Power BI reports
- PDF and Excel exports
- CSV/Excel ingestion with manager approval before stakeholder publication
- Activity logging for authentication and dashboard use
- SQLAlchemy models and Flask-Migrate migrations

## Data-import flow

```text
Admin upload → ImportedData staging → Manager review → Published stakeholder metrics
```

## Local setup

Python 3.11 or newer is recommended.

```bash
cd server
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python init_db.py
python app.py
```

Open `http://localhost:5001`.

`init_db.py` rebuilds database tables; do not run it against data you need to preserve.

## Repository structure

```text
server/
├── app.py          Application factory and entry point
├── blueprints/     Authentication, users, dashboards, and public routes
├── forms/          WTForms and validation
├── models/         SQLAlchemy domain models
├── init_db.py      Local database initialization
└── requirements.txt
frontend/
├── static/         Styles, scripts, and visual assets
└── templates/      Jinja views
```

## Configuration

Keep the Flask secret, mail credentials, database URL, and Power BI embed configuration outside source control. Use a long random session key and HTTPS in production. The application can optionally load SharePoint data when the related variables and dependency are configured.

## Attribution and license

Based on [Nafisa Anjum Ahmed's PowerBI-Dashboard](https://github.com/nafisanafu15/PowerBI-Dashboard) and substantially modified by `wnzid`.

Licensed under the [MIT License](LICENSE).
