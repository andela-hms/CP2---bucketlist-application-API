import os
import json
from run_app import app, db

from base_test import BaseTestCase
from models import User, BucketList, Item

URL = "/bucketlists/"

class BucketListTestCase(BaseTestCase):
    """ Test suite for BucketList API """
    def setUp(self):
        """ Create resources to get auth token for login and access """
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

        headers = json.dumps({"Content-Type":"application/json","Accept":"application/json"})
        response = self.client.post("/auth/login/", data=data, content_type="application/json")
        # response = response.data.decode()
        data = json.loads(response.data.decode())
        auth_token = data['auth_token']

        self.headers = {
            'Authorization':'Token ' + auth_token,
            'Content-Type': 'application/json',
            'Accept':'application/json',
        }

    def test_create_bucket_list(self):
        """ Tests whether a user can create a new bucketlist """
        new_bucket_list = json.dumps(dict(
            bucketlist_name="Kenya"
        ))

        headers = json.dumps({"Content-Type":"application/json","Accept":"application/json"})
        response = self.client.post(URL, data=new_bucket_list, content_type="application/json", headers=self.headers)
        self.assertIn("bucketlist_name", response.data.decode())

    def tearDown(self):
        """ Clear resources after tests are run """
        db.session.remove()
        db.drop_all()
        os.remove('test.db')