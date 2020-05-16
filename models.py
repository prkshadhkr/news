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
    source_id = db.Column(db.Text)
    author = db.Column(db.Text)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text)
    published_at = db.Column(db.Text)
    content = db.Column(db.Text)

    #relationships for article_boards
    article_boards = db.relationship('ArticleBoard', backref="articles")


class ArticleBoard(db.Model):
    """article_boards table"""

    __tablename__ = 'article_boards'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, 
                        db.ForeignKey('articles.id', ondelete="cascade"), nullable=False)
    board_id = db.Column(db.Integer, 
                        db.ForeignKey('boards.id', ondelete="cascade"), nullable=False)
    is_read = db.Column(db.Boolean, default=False)

 
class Board(db.Model):
    """boards table"""

    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete="cascade"), nullable=False)
    name = db.Column(db.Text, nullable=False)

    #relationships for article_boards
    article_boards = db.relationship('ArticleBoard', backref="boards", cascade="all, delete-orphan")

    #through relationships for articles
    articles = db.relationship('Article', 
                        secondary='article_boards',                         
                        backref='boards')


class Feed(db.Model):
    """feeds table"""

    __tablename__ = 'feeds'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete="cascade"), nullable=False)
    name = db.Column(db.Text, nullable=False)

    #relationships for source_feeds
    source_feeds = db.relationship('SourceFeed', backref="feeds", cascade="all, delete-orphan") 

    #through relationships for sources
    sources = db.relationship('Source', 
                        secondary='source_feeds',                         
                        backref='feeds')


class SourceFeed(db.Model):
    """source_feeds table"""

    __tablename__ = 'source_feeds'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Text,
                        db.ForeignKey('sources.id', ondelete="cascade"), nullable=False)
    feed_id = db.Column(db.Integer, 
                        db.ForeignKey('feeds.id', ondelete="cascade"), nullable=False)

    # not sure if we are going to use following
    def to_serialize(self):
        """Serialize sourcefeed."""

        return {
            "id": self.id,
            "source_id": self.source_id,
            "feed_id": self.feed_id
        }


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

    #relationships for source_feeds
    source_feeds = db.relationship('SourceFeed', backref="sources")


class User(db.Model):
    """users table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, default="us")

    #relationships for feeds
    feeds = db.relationship('Feed', backref="users", cascade="all, delete-orphan")

    #relationships for boards
    boards = db.relationship('Board', backref="users", cascade="all, delete-orphan")

    @classmethod
    def signup(cls, username, email, password, country):
        """Sign up user.

        Hashes password and adds user to system.
        """
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            country=country
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