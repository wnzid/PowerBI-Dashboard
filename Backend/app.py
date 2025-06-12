from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from models import db, User, Role
from db import DB_PATH
from auth import auth_bp
from dashboard import dashboard_bp
from main_routes import main_bp
from extensions import limiter


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + DB_PATH)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)
    limiter.init_app(app)

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

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    enable_https = os.getenv('ENABLE_HTTPS', '0').lower() in {'1', 'true', 'yes'}
    ssl_context = 'adhoc' if enable_https else None
    app.run(debug=True, port=5001, ssl_context=ssl_context)
