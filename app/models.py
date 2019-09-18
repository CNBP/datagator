from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """
    Database Model Class
    """

    # User database model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    # Print object from this class
    def __repr__(self):
        return "<usr {}>".format(self.username)

    # Hash generation.
    def set_password(self, password):
        """
        Function to set the password for the user database class
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    # hash checking.
    def check_password(self, password):
        """
        Function to check the password for the user database class
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """
        Return the avatar up to a particular size.
        :param size:
        :return:
        """
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        link = f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"
        return link


class Entry(db.Model):
    """
    This is used to model the data entry from the user regarding the scans.
    """

    id = db.Column(db.Integer, primary_key=True)
    MRN = db.Column(db.Integer)
    CNBPID = db.Column(db.String(10))
    birth_weight = db.Column(db.String(140))
    birth_date = db.Column(db.Date)
    birth_time = db.Column(db.Time)
    mri_date = db.Column(db.Date)
    mri_reason = db.Column(db.String)

    # Many more fields to add here.
    mri_dx = db.Column(db.String)

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # used to associate who entered this entry.

    def __repr__(self):
        return "<Entry {}>".format(self.body)


class Post(db.Model):
    """
    This is the post class, used to model the data brought on
    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)
