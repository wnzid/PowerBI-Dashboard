from flask import Flask
from db import init_db
from auth import auth_bp
from dashboard import dashboard_bp
from main_routes import main_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "your_secret_key"  # Needed for session management

    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
