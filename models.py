"Models for notes app."

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


def connect_db(app):
    """Connect database to app"""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for User"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password and return user"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name)


    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct
        Return user if valid; else return False"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Note(db.Model):
    """Model for notes"""

    __tablename__ = 'notes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        auto_increment=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    owner_username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False
    )
# TODO: owner instead of user for consistency
    user = db.relationship('User', backref='notes')