import os
import json
from run_app import app, db

from base_test import BaseTestCase
from models import User, BucketList, Item

class BucketListTestCase(BaseTestCase):
    """ Test suite for ItemAPI """
    def setUp(self):
        """ Create resources to get auth token for login and access """
        db.create_all()

        new_user = User(
            username='testuser',
            email_address="test@newguy.com"
        )
        new_user.hash_this_pass("thispass")
        db.session.add(new_user)
        db.session.commit()

        data = json.dumps(dict(
            email="test@newguy.com",
            password="thispass"
        ))

        response = self.client.post("/auth/login/", data=data, content_type="application/json")
        # response = response.data.decode()
        data = json.loads(response.data.decode())
        auth_token = data['auth_token']

        self.headers = {
            'Authorization':'Token ' + auth_token,
            'Content-Type': 'application/json',
            'Accept':'application/json',
        }

        # create new bucketlist
        new_bucket_list = json.dumps(dict(
            bucketlist_name="Kenya"
        ))

        url = "/bucketlists/"

        self.client.post(url, data=new_bucket_list, \
        content_type="application/json", headers=self.headers)

    def test_create_new_item(self):
        """ Tests whether a user can create a new item based on a bucketlist_id """
        new_item = json.dumps(dict(
            item_name="Go on a safari"
        ))

        url = "/bucketlists/1/items/"

        response = self.client.post(url, data=new_item, \
        content_type="application/json", headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertTrue(data["item_name"] == "Go on a safari")

    def tearDown(self):
        """ Clear resources after tests are run """
        db.session.remove()
        db.drop_all()
        os.remove('test.db')
