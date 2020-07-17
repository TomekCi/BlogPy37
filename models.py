from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


"""
python manage.py db init
                    migrate
                    upgrade 
"""


class Users(BaseModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    emailAddress = db.Column(db.String(40), unique=True, nullable=False)
    userName = db.Column(db.String(20), nullable=False)
    passwordSalt = db.Column(db.String(30), nullable=False)
    passwordHash = db.Column(db.String(30), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", back_populates="users")

    children = db.relationship("Comments", back_populates="users")


class Author(BaseModel, db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    authorDescription = db.Column(db.String(80), nullable=False)

    users = db.relationship("Users", uselist=False, back_populates="author")
    posts = db.relationship("posts", back_populates="author")


class Posts(BaseModel, db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.String(400), nullable=False)

    authorP_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    authorP = db.relationship("author", back_populates="posts")

    children = db.relationship("comments", back_populates="posts")


class Comments(BaseModel, db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post = db.relationship('Posts', backref='posts')
    user = db.relationship('Users', backref='user')
    text = db.Column(db.String(60), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    parent = db.relationship("Posts", back_populates="comments")

    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent = db.relationship("Users", back_populates="comments")
