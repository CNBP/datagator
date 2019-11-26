from app import db, login
from flask import current_app, url_for
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from time import time
import sqlalchemy as sa
from sqlalchemy_utils import EncryptedType, URLType
from sqlalchemy_utils.types.encrypted.encrypted_type import FernetEngine
import os
from dotenv import load_dotenv


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# IMPORTANT!
# Whenever a change made below to the db.columns etc, make sure to add a migration script. and run it.
# e.g.

# ```
# flask db migrate -m "COMMENTS HERE"
# flask db upgrade
# ```


class Post(db.Model):
    """
    This is the post class, used to model the data brought on
    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Post {self.body}>"


class User(UserMixin, db.Model):
    """
    Database Model Class
    """

    # This table has a column to track follower number 1 to follower number 2
    # This table is not a model.
    followers = db.Table(
        "followers",
        db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
        db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
    )

    # User database model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    # new fields to be migrated
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # retrieve the list of users that this current user is following.
    followed = db.relationship(
        "User",  # right side entity to be linked. Left side is the parent class, which is also user.
        secondary=followers,  # association table
        primaryjoin=(followers.c.follower_id == id),  # left side, follower
        secondaryjoin=(followers.c.followed_id == id),  # right side, follower
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    def created_entries(self):
        """
        This method returns all the posts of this user currently follows.
        :return:
        """
        # Get followed posts.
        entries = Entry.query.filter_by(user_id=self.id)

        # Return all the entries by this user in descending temporal order
        return entries.order_by(Entry.timestamp.desc())

    def followed_posts(self):
        """
        This method returns all the posts of this user currently follows.
        :return:
        """

        # This table has a column to track follower number 1 to follower number 2
        # This table is not a model.
        followers = db.Table(
            "followers",
            db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
            db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
        )

        # Get followed posts.
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id)

        # Get self posts
        own = Post.query.filter_by(user_id=self.id)

        # Return the combined results ordere by post time.
        return followed.union(own).order_by(Post.timestamp.desc())

    # Print object from this class
    def __repr__(self):
        return f"<usr {self.username}>"

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

    def follow(self, user):
        """
        Used to add a follow relationship to the other user.
        :param user:
        :return:
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """
        Used to remove a follow relationship to the other user.
        :param user:
        :return:
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """
        Return the status of the is_following relationship
        :param user:
        :return:
        """
        # This table has a column to track follower number 1 to follower number 2
        # This table is not a model.
        followers = db.Table(
            "followers",
            db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
            db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
        )

        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def get_reset_password_token(self, expires_in=600):
        """
        Get reset token, with the id encoded and expiring time.
        :param expires_in:
        :return:
        """
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        """
        Verify the token then return UserID as authenticated.
        :param token:
        :return:
        """
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )[
                "reset_password"
            ]  # get the value from that dictionary.
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        """
        A way to represent the data base object as JSON dictionary
        :param include_email:
        :return:
        """
        data = {
            "id": self.id,
            "username": self.username,
            "last_seen": self.last_seen.isoformat() + "Z",
            "about_me": self.about_me,
            "post_count": self.posts.count(),
            "follower_count": self.followers.count(),
            "followed_count": self.followed.count(),
            "_links": {
                "self": url_for("api.get_user", id=self.id),
                #                "followers": url_for("api.get_followers", id=self.id),
                #                "followed": url_for("api.get_followed", id=self.id),
                "avatar": self.avatar(128),
            },
        }
        if include_email:
            data["email"] = self.email
        return data

    def from_dict(self, data, new_user=False):
        """
        Convert data from a dictionary object.
        :param data:
        :param new_user:
        :return:
        """
        for field in ["username", "email", "about_me"]:
            if (
                field in data
            ):  # check to makes sure those fields exist in the data received.
                setattr(self, field, data[field])
            if (
                new_user and "password" in data
            ):  # only set password if we have received them.
                self.set_password(data["password"])


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
    mri_dx = db.Column(db.String)  # JSON string
    dicharge_diagoses = db.Column(db.String)
    mri_age = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # used to associate who entered this entry.

    def entries(self, input_user_id):
        """
        This method returns all the posts of this user currently follows.
        :return:
        """
        # Get self own entries
        own = Entry.query.filter_by(user_id=input_user_id)

        # Return the combined results ordere by post time.
        return own.order_by(Entry.timestamp.desc())

    def __repr__(self):
        return f"<Entry {self.id}>"


class DICOMTransitConfig(db.Model):
    """
    This is used to model the configuration entry from the user regarding DICOMTransit Operation.
    """

    # Get the encryption key from the env.
    load_dotenv()
    key = os.getenv("encryption_key")

    # Inspired from: https://stackoverflow.com/questions/49560609/sqlalchemy-encrypt-a-column-without-automatically-decrypting-upon-retrieval
    id = db.Column(db.Integer, primary_key=True)  # hidden
    LORISurl = db.Column(URLType)
    LORISusername = db.Column(db.String)
    LORISpassword = db.Column(EncryptedType(db.Unicode, key, FernetEngine))

    timepoint_prefix = db.Column(db.String)
    institutionID = db.Column(db.String)
    institutionName = db.Column(db.String)
    projectID_dic = db.Column(db.String)
    LocalDatabasePath = db.Column(db.String)
    LogPath = db.Column(db.String)
    ZipPath = db.Column(db.String)

    # Orthanc configuration
    DevOrthancIP = db.Column(db.String)
    DevOrthancUser = db.Column(db.String)
    DevOrthancPassword = db.Column(db.String)

    ProdOrthancIP = db.Column(db.String)
    ProdOrthancUser = db.Column(db.String)
    ProdOrthancPassword = db.Column(db.String)

    # RedCap related data control.

    REDCAP_TOKEN_CNN_ADMISSION = db.Column(db.String)
    REDCAP_TOKEN_CNN_BABY = db.Column(db.String)
    REDCAP_TOKEN_CNN_MOTHER = db.Column(db.String)
    REDCAP_TOKEN_CNN_MASTER = db.Column(db.String)
    REDCAP_TOKEN_CNFUN_PATIENT = db.Column(db.String)
    REDCAP_API_URL = db.Column(db.String)
    CNN_CONNECTION_STRING = db.Column(db.String)
    CNFUN_CONNECTION_STRING = db.Column(db.String)
    USE_LOCAL_HOSPITAL_RECORD_NUMBERS_LIST = db.Column(db.Integer)
    NUMBER_OF_RECORDS_PER_BATCH = db.Column(db.Integer)

    # RedCap export related data control
    REDCAP_EXPORT_ENABLED = db.Column(db.String)

    # MySQL
    MYSQL_EXPORT_ENABLED = db.Column(db.String)
    MYSQL_EXPORT_HOST = db.Column(db.String)
    MYSQL_EXPORT_PORT = db.Column(db.String)
    MYSQL_EXPORT_DATABASE = db.Column(db.String)
    MYSQL_EXPORT_USER = db.Column(db.String)
    MYSQL_EXPORT_PASSWORD = db.Column(db.String)

    # CouchDB
    COUCHDB_EXPORT_ENABLED = db.Column(db.String)
    COUCHDB_EXPORT_HOST = db.Column(db.String)
    COUCHDB_EXPORT_PORT = db.Column(db.String)
    COUCHDB_EXPORT_DATABASE = db.Column(db.String)
    COUCHDB_EXPORT_USER = db.Column(db.String)
    COUCHDB_EXPORT_PASSWORD = db.Column(db.String)

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # hidden

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # used to associate who entered this entry. # hidden

    def __repr__(self):
        return f"<DICOMTransitConfig {self.id} by {self.user_id} on {self.timestamp}>"
