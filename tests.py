from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from config import Config


class UserModelCase(unittest.TestCase):
    def setUp(self):
        """
        Setup method to setup a temporary database.
        :return:
        """
        self.app = create_app(TestConfig)
        # Ensure the proper database hookup.
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Remove the database afterward
        :return:
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username="susan")
        u.set_password("user")
        self.assertFalse(u.check_password("dog"))
        self.assertTrue(u.check_password("user"))

    def test_avatar(self):
        u = User(username="john", email="john@example.com")
        self.assertEqual(
            u.avatar(128),
            (
                "https://www.gravatar.com/avatar/"
                "d4c74594d841139328695756648b6bd6"
                "?d=identicon&s=128"
            ),
        )

    def test_follow(self):
        """
        Test the follow function .
        :return:
        """

        # Setup two users.
        u1 = User(username="john", email="john@example.com")
        u2 = User(username="susan", email="susan@example.com")
        # Add to db.
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # Ensure now of them have any follower or followed.
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        # Make u1 follow u2
        u1.follow(u2)
        db.session.commit()
        # check u1 following
        self.assertTrue(u1.is_following(u2))
        # Check u1 followed count
        self.assertEqual(u1.followed.count(), 1)
        # Check u1 followed first person should be SUSAN
        self.assertEqual(u1.followed.first().username, "susan")
        # Check u2 for follower count
        self.assertEqual(u2.followers.count(), 1)
        # Check u2 follower name is John.
        self.assertEqual(u2.followers.first().username, "john")

        # Reverse. Unfollow.
        u1.unfollow(u2)
        db.session.commit()
        # Assert no longer following and all counts are zero.
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # Create four userso

        u1 = User(username="john", email="john@example.com")
        u2 = User(username="susan", email="susan@example.com")
        u3 = User(username="mary", email="mary@example.com")
        u4 = User(username="david", email="david@example.com")

        db.session.add_all([u1, u2, u3, u4])

        # Create four posts
        now = datetime.utcnow()
        p1 = Post(
            body="post from john", author=u1, timestamp=now + timedelta(seconds=1)
        )
        p2 = Post(
            body="post from susan", author=u2, timestamp=now + timedelta(seconds=4)
        )
        p3 = Post(
            body="post from mary", author=u3, timestamp=now + timedelta(seconds=3)
        )
        p4 = Post(
            body="post from david", author=u4, timestamp=now + timedelta(seconds=2)
        )

        # Setup the followers:
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david

        db.session.commit()

        # Check the followed posts.

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


if __name__ == "__main__":
    unittest.main(verbosity=2)
