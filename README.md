# Power BI Dashboard Portal

A Flask web application for hosting Power BI dashboards for the Analytics Institute of Australia. The portal provides user registration, secure login and role-based dashboards for managers and stakeholders.

## Features

- Landing page highlighting real-time KPIs, multi-source integration and advanced filtering
- User registration with hashed passwords and role selection
- Secure login and session management
- Managerial dashboard with sample charts and Power BI integration placeholders
- Stakeholder dashboard (coming soon)
- Reporting and help pages
- SQLite database for storing user accounts

## Getting Started

### Requirements

- Python 3.11+
- Virtualenv or a similar tool

### Installation

```bash
# Clone the repository
 git clone <repo-url>
 cd PowerBI-Dashboard/Backend

# Create and activate a virtual environment
 python3 -m venv venv
 source venv/bin/activate

# Install dependencies
 pip install -r requirements.txt

# Initialize the database
 python init_db.py
```

### Running the Application

```bash
python app.py
```

The application starts on **http://localhost:5001**. Visit this URL in your browser to see the landing page. Use the **Register** link to create an account. Managers are redirected to the managerial dashboard; stakeholders go to their own dashboard.

### Viewing Registered Users

A helper script prints all registered users from the SQLite database:

```bash
python view-users.py
```

## Project Structure

```
Backend/              # Flask application
├── app.py            # Main app entry point
├── db.py             # SQLite helpers
├── init_db.py        # Database initialization script
├── view-users.py     # Utility to inspect stored users
├── requirements.txt  # Python dependencies
├── static/           # CSS, JavaScript and images
└── templates/        # Jinja2 HTML templates
```

## What's New (Modified Version by wnzid)

The following improvements have been made to enhance the functionality, maintainability, and security of the original project:

#### Backend & Security Enhancements
- Introduced `db.py` and `init_db.py` for better database separation and initialization
- Replaced static login with secure password hashing using `werkzeug.security`
- Added dynamic user authentication and role-based routing (manager vs stakeholder)

#### Utility Scripts & Maintenance
- Added `view-users.py` to help inspect and debug registered users in the database
- Cleaned up backend folder structure and removed redundant or unused files

#### Documentation & Licensing
- Created this detailed `README.md` with step-by-step setup instructions
- Added an MIT License to comply with open-source distribution and ensure proper attribution

These changes aim to make the application more production-ready and accessible for further development or academic use.

---

## Acknowledgements

This project is based on [PowerBI-Dashboard](https://github.com/nafisanafu15/PowerBI-Dashboard) by Nafisa Anjum Ahmed and is licensed under the [MIT License](https://opensource.org/licenses/MIT). Significant modifications and improvements have been made by **wnzid**.


