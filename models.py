from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as hash_alg


db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        # Define a base way to print models
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })
"""
    def json(self):
        # Define a base way to jsonify models, dealing with datetime objects
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }"""


class User(BaseModel, UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    register_date = db.Column(db.DateTime, server_default=db.func.now())

    @staticmethod
    def hash_password(password):
        return hash_alg.encrypt(password)

    def verify_password(self, pwd_hash):
        return hash_alg.verify(pwd_hash, self.password_hash)

