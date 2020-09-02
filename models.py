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

userroles = db.Table('userroles',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('roles.role_id'))
)


class Users(BaseModel, UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    register_date = db.Column(db.DateTime, server_default=db.func.now())
    # roles = db.relationship('Roles', secondary='userroles')
    role_assignations = db.relationship('Roles', secondary=userroles, backref=db.backref('assignations', lazy='dynamic'))

    @staticmethod
    def hash_password(password):
        return hash_alg.encrypt(password)

    def verify_password(self, pwd_hash):
        return hash_alg.verify(pwd_hash, self.password_hash)


class Roles(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class Posts(BaseModel, db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
    author = db.Column(db.String, nullable=False)
