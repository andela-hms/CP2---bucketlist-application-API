import os
import json
from flask_testing import TestCase


from run_app import app, db
from models import User, BucketList, Item

class BaseTestCase(TestCase):
    """ Initialize app and setup db resources """
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        """ Initialize resources for our tests """
        db.create_all()
        new_user = User(
            username='newguy',
            email_address="test@user.com"
        )
        new_user.hash_this_pass("thispass")
        db.session.add(new_user)
        db.session.commit()

        data = json.dumps(dict(
            email="test@user.com",
            password="thispass"
        ))

        response = self.client.post("/api/v1.0/auth/login/", \
        data=data, content_type="application/json")
        data = json.loads(response.data.decode())
        auth_token = data['auth_token']

        self.headers = {
            'Authorization':'Token ' + auth_token,
            'Content-Type': 'application/json',
            'Accept':'application/json',
        }

    def tearDown(self):
        """ Clear resources after tests are run """
        db.session.remove()
        db.drop_all()
        os.remove('test.db')

