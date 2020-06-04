"""
1. Register, Login
2. Shorten the URL
3. API
"""

import unittest
from app import app # importing app variable from app.py

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def register(self, email, password, confirmation):
        return self.app.post("/register", data=dict(email=email, password=password, confirmation=confirmation))

    def test_register(self):
        # register without password
        rv = self.register("fake@example.com", "", "abc")
        assert b"please fill out all fields" in rv.data

        # register without username
        rv = self.register("", "hi", "abc")
        assert b"please fill out all fields" in rv.data

        # register without confirmation
        rv = self.register("fake@example.com", "hi", "")
        assert b"please fill out all fields" in rv.data

        # register wrong confirmation
        rv = self.register("fake@example.com", "hi", "abc")
        assert b"password confirmation doesn't match password" in rv.data

        # register with existing credentials
        rv = self.register("dev@example.com", "hi", "hi")
        print(rv.data)
        assert b"user already registered" in rv.data

        # register success
        rv = self.register("code@example.com", "hi", "hi")
        print(rv.data)
        assert b"registered successfully!" in rv.data

    def test_api(self):
        rv = self.app.get("/api?custom=hello")
        assert str(200) in str(rv.get_json()["code"])


if __name__ == "__main__":
    unittest.main()