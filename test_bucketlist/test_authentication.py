import json
from base_test import BaseTestCase

URL = "/auth/"
class AuthTestCase(BaseTestCase):
    def test_login(self):
        """ Tests whether a user can login """
        data = json.dumps(dict(
            email="test@user.com",
            password="thispass"
        ))

        response = self.client.post(URL+"login/", data=data, content_type="application/json")
        self.assertIn("auth_token",response.data.decode())

    def test_register(self):
        """ Tests whether a new user can be created successfully """
        data = json.dumps(dict(
            username="new_user",
            email="new_user@user.com",
            password="newuserpass"
            ))

        response = self.client.post(URL+"register/", data=data, content_type="application/json")
        self.assertIn("Registration successful",response.data.decode())
