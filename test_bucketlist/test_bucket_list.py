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

        response = self.client.post("/auth/login/", data=data, content_type="application/json")
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

        response = self.client.post(URL, data=new_bucket_list, \
        content_type="application/json", headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertTrue(data["bucketlist_name"] == "Kenya")

    def test_get_bucketlists(self):
        """ Tests whether a user can GET created bucketlists """
        response = self.client.get(URL, content_type="application/json", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """ Clear resources after tests are run """
        db.session.remove()
        db.drop_all()
        os.remove('test.db')
