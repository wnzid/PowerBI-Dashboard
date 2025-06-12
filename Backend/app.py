from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from extensions import mail
from models import db, User, Role, ActivityLog
from db import DB_PATH
from auth import auth_bp
from dashboard import dashboard_bp
from main_routes import main_bp


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
        if Role.query.count() == 0:
            db.session.add_all([Role(name='Manager'), Role(name='Stakeholder')])
            db.session.commit()

    admin = Admin(app, name='Admin', template_mode='bootstrap4')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(ActivityLog, db.session))

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
