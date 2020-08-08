from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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
    # name = db.Column(db.String(20), nullable=False)
    # surname = db.Column(db.String(30), nullable=False)
    emailaddress = db.Column(db.String(40), unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    passwordhash = db.Column(db.String(30), nullable=False)
    register_date = db.Column(db.DateTime, server_default=db.func.now())

    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(BaseModel, db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


"""
python manage.py db init
                    migrate
                    upgrade 
"""

"""
class User(BaseModel, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    emailAddress = db.Column(db.String(40), unique=True, nullable=False)
    userName = db.Column(db.String(20), nullable=False)
    passwordHash = db.Column(db.String(30), nullable=False)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
"""

"""
class Author(BaseModel, db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    authorDescription = db.Column(db.String(80), nullable=False)

    users = db.relationship("Users", uselist=False, back_populates="author")
    posts = db.relationship("posts", back_populates="author")
"""


"""
class Comments(BaseModel, db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    #post = db.relationship('Posts', backref='posts')
    #user = db.relationship('Users', backref='user')
    text = db.Column(db.String(60), nullable=False)

    posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    posts = db.relationship("Posts", back_populates="comments")

    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship("Users", back_populates="comments")
"""

