from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask Tests."""
    def setUp(self):
        """Do this before every test."""

        # get the Flask test client
        self.client = app.test_client()
        # Show Flask errors that happen during testing
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b'<label for="floatingInput">Email address</label>', result.data)

class FlaskTestsDatabase(TestCase):

    def setUp(self):
        """Do this before every test."""

        # get the Flask test client
        self.client = app.test_client()
        # Show Flask errors that happen during testing
        app.config['TESTING'] = True

        # connect to database
        connect_to_db(app, "postgresql:///testdb")

        # create tables and populate with dummy data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['user_fname'] = 'Chani'
            

    def tearDown(self):
        """Do after every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login", data={"email": "chani@arrakis.com","password": "sihaya"},
        follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1 class="display-5">Welcome, Chani!</h1>', result.data)

    def test_get_user_reviews(self):

        result = self.client.get("/all_user_reviews")
        self.assertIn(b"LGBTQIA", result.data)

    def test_restroom_reviews(self):

        result = self.client.get("/all_restroom_reviews", data={"bathroom_id": "01", "bathroomName": "goodRR"})
        self.assertIn(b"<h1>Here are the reviews for goodRR!</h1>", result.data)
    
class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess["user_fname"] = "Chani"

    def test_user_page(self):
        """Test important page."""

        result = self.client.get("/user_page")
        self.assertIn(b'<h1 class="display-5">Welcome, Chani!</h1>', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()