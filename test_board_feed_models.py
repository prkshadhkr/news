
"""Feed and Board model tests."""

# run these tests like:
#
#    python -m unittest test_board_feed_models.py


import os
from unittest import TestCase

from models import db, User, Feed, Board

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///news_db_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()



class FeedBoardModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "testing@test.com", "password", 'gb')
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()


    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_feed_model(self):
        """Does basic model work?"""
        
        f = Feed(
            name="test feed name",
            user_id=self.uid
        )

        db.session.add(f)
        db.session.commit()

        # User should have 1 feed created
        self.assertEqual(len(self.u.feeds), 1)
        self.assertEqual(self.u.feeds[0].name, "test feed name")



    def test_board_model(self):
        """Does basic model work?"""
        
        b = Board(
            name="test board name",
            user_id=self.uid
        )

        db.session.add(b)
        db.session.commit()

        # User should have 1 board created
        self.assertEqual(len(self.u.boards), 1)
        self.assertEqual(self.u.boards[0].name, "test board name")