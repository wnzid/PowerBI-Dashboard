# Power BI Dashboard Portal

A Flask web application for hosting Power BI dashboards for the Analytics Institute of Australia. The portal provides user registration, secure login and role-based dashboards for managers and stakeholders.

## Features

- Landing page highlighting real-time KPIs, multi-source integration and advanced filtering
- User registration with hashed passwords and role selection
- Secure login and session management
- Built-in CSRF protection for all forms
- Automatic HTTPS redirect in production
- Password reset via email
- Profile editing and password change
- Admin panel for managing users and roles
- Roles stored in the database for dynamic role-based access control
- Activity logging of successful and failed logins and dashboard usage
- Managerial dashboard with interactive Power BI embed
- Stakeholder dashboard with interactive Power BI embed and export to PDF or Excel
- Reporting and help pages
- SQLAlchemy with SQLite and Flask-Migrate for database management

## Getting Started

### Requirements

- Python 3.11+
- Virtualenv or a similar tool

### Installation

```bash
# Clone the repository
 git clone <repo-url>
 cd PowerBI-Dashboard/server

# Create and activate a virtual environment
 python3 -m venv venv
 source venv/bin/activate

# Install dependencies
 pip install -r requirements.txt

# Initialize the database (drops existing tables)
 python init_db.py
```

### Running the Application

```bash
python app.py
```

The application starts on **http://localhost:5001**. Visit this URL in your browser to see the landing page. Use the **Register** link to create an account. Managers are redirected to the managerial dashboard; stakeholders go to their own dashboard.

### Default Admin Account

An administrator account is created automatically when the application starts if it doesn't already exist

Only that user has access to the Flask-Admin interface.

New users can register only as Manager or Stakeholder. The Admin role is
reserved for the predefined account and is hidden from the registration form.

### Viewing Registered Users

A helper script prints all registered users from the SQLite database:

```bash
python view-users.py
```

## Project Structure

```
server/               # Flask backend
├── app.py            # Application factory and entry point
├── blueprints/       # Flask blueprints
│   ├── auth.py       # Authentication routes
│   ├── dashboard.py  # Dashboard routes
│   └── main_routes.py  # General site routes
├── forms/            # WTForms definitions
├── models/           # SQLAlchemy models
├── db.py             # Database path configuration
├── init_db.py        # Database initialization script
├── view-users.py     # Utility to inspect stored users
├── requirements.txt  # Python dependencies
frontend/             # Client-side assets
├── static/           # CSS, JavaScript and images
└── templates/        # Jinja2 HTML templates
```

## What's New (Final Modified Version by wnzid)

#### Functional Enhancements
- Fully embedded interactive Power BI dashboards for both Manager and Stakeholder roles
- Added PDF and Excel export functionality on dashboards
- Integrated user activity logging (e.g., login attempts, dashboard usage)
- Added password reset via email
- Users can edit profile and change password
- Included Flask-Admin interface for managing users and roles

#### Security & Role Management
- Role-based access now dynamically managed via database (not hardcoded)
- Strengthened login flow with additional logging and role validation
- Improved `.env` configuration and `.gitignore` for safer environment variable handling

#### Database & Code Quality
- Replaced raw SQL with **SQLAlchemy ORM**
- Integrated **Flask-Migrate** for smooth schema updates and DB version control
- Cleaned up and modularized database interactions

#### UI/UX and Documentation
- Refined landing page visuals and dashboard icons
- Updated README with full deployment instructions

---

## Acknowledgements

This project is based on [PowerBI-Dashboard](https://github.com/nafisanafu15/PowerBI-Dashboard) by Nafisa Anjum Ahmed and is licensed under the [MIT License](https://opensource.org/licenses/MIT). Significant modifications and improvements have been made by **wnzid**.


