from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    users = User.query.all()
    print("All registered users:")
    for user in users:
        print(user.id, user.email, user.role)
