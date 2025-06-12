from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from extensions import mail
from models import db, User, Role, ActivityLog
from werkzeug.security import generate_password_hash
from flask_login import current_user
from flask import redirect, url_for
from db import DB_PATH
from auth import auth_bp
from dashboard import dashboard_bp
from main_routes import main_bp


class SecureModelView(ModelView):
    """Restrict Flask-Admin views to predefined admin users."""

    def is_accessible(self) -> bool:
        return (
            current_user.is_authenticated
            and current_user.role
            and current_user.role.name.lower() == "admin"
        )

    def inaccessible_callback(self, name: str, **kwargs):
        return redirect(url_for("auth.login"))


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.setdefault('MAIL_SERVER', 'localhost')
    app.config.setdefault('MAIL_PORT', 8025)
    app.config.setdefault('MAIL_DEFAULT_SENDER', 'noreply@example.com')

    mail.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()
        for role_name in ("Admin", "Manager", "Stakeholder"):
            if not Role.query.filter_by(name=role_name).first():
                db.session.add(Role(name=role_name))
        db.session.commit()

        admin_role = Role.query.filter_by(name="Admin").first()
        if admin_role and not User.query.filter_by(email="admin@gmail.com").first():
            hashed_pw = generate_password_hash("admin123456789")
            admin_user = User(email="admin@gmail.com", password=hashed_pw, role_id=admin_role.id)
            db.session.add(admin_user)
            db.session.commit()

    admin = Admin(app, name='Admin', template_mode='bootstrap4')
    admin.add_view(SecureModelView(User, db.session))
    admin.add_view(SecureModelView(Role, db.session))
    admin.add_view(SecureModelView(ActivityLog, db.session))

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
