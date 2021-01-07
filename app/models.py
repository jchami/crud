from app import db
from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt


class User(db.Model):
    """Model for storing user data in database."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise(e)
    
    def generate_token(self, token_expiration):
        return create_access_token(
            identity={'id': self.id, 'email': self.email},
            expires_delta=token_expiration
        )

    def __repr__(self):
        return '<User: {}>'.format(self.email)


class ActivationRequest(db.Model):
    """Model for storing data on activation requests in database."""

    __tablename__ = 'activation_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(256), nullable=False)
    approved = db.Column(db.Boolean)

    def __init__(self, user_id, company_name):
        self.user_id = user_id
        self.company_name = company_name
        self.approved = None

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise(e)

    def delete(self):
        db.session.delete(self)
        db.session.commit()