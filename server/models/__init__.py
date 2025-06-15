from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Role {self.name}>"


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', backref='users')

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    activity_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='activities')

    def __repr__(self) -> str:
        return f"<Activity {self.activity_type} user={self.user_id}>"


class CSVFile(db.Model):
    """Metadata about uploaded CSV files."""
    __tablename__ = 'csv_files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending/approved/declined
    active = db.Column(db.Boolean, default=True)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    uploaded_by = db.relationship('User', backref='csv_files')

    def __repr__(self) -> str:
        return f"<CSVFile {self.filename} status={self.status}>"


class ImportedData(db.Model):
    """Store rows imported from CSV files."""
    __tablename__ = 'imported_data'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    csv_file_id = db.Column(db.Integer, db.ForeignKey('csv_files.id'), nullable=True)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    csv_file = db.relationship('CSVFile', backref='rows')
    uploaded_by = db.relationship('User', backref='imports')

    def __repr__(self) -> str:
        return f"<ImportedData {self.id} approved={self.approved}>"
