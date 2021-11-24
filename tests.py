from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask Tests"""
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

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login", data={"email": "chani@arrakis.com","password": "sihaya"},
        follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1 class="display-5">Welcome, {{ fname }}!</h1>', result.data)






















if __name__ == "__main__":
    import unittest

    unittest.main()