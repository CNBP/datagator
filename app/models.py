from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# IMPORTANT!
# Whenever a change made below to the db.coluns etc, make sure to add a migration script. and run it.
# e.g.

# ```
# flask db migrate -m "COMMENTS HERE"
# flask db upgrade
# ```


# This table has a column to track follower number 1 to follower number 2
# This table is not a model.
followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
)


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

    def followed_posts(self):
        """
        This method returns all the posts of this user currently follows.
        :return:
        """
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
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0


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
