"""SQLAlchemy models for News Aggretion."""

# from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


#################  DATABASE SCHEMA  ####################

class Article(db.Model):
    """articles table"""

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_name = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)


class Board(db.Model):
    """boards table"""

    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete="cascade"))
    article_id = db.Column(db.Integer, 
                        db.ForeignKey('articles.id', ondelete="cascade"))
    name = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)


class Feed(db.Model):
    """feeds table"""

    __tablename__ = 'feeds'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete="cascade"))
    source_id = db.Column(db.Text, 
                        db.ForeignKey('sources.id', ondelete="cascade"))
    name = db.Column(db.Text, nullable=False)
 

class Source(db.Model):
    """sources table"""

    __tablename__ = 'sources'

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    language = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)


class User(db.Model):
    """users table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    #through relationships between users and articles via boards and users and sources via feeds
    articles = db.relationship(
        'Article', secondary="boards", backref="users")
    sources = db.relationship(
        'Source', secondary="feeds", backref="users")


    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user



    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False