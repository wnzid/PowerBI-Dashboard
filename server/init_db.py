"""Database initialization utility for the Flask application."""

from app import create_app
from models import db


def init_database(app) -> None:
    """Recreate all tables for a clean database state."""
    db.drop_all()
    db.create_all()
    print(f"Database initialized at {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        init_database(app)
