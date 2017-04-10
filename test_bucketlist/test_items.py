import os
import json
from run_app import app, db

from base_test import BaseTestCase
from models import User, BucketList, Item

class ItemTestCase(BaseTestCase):
    """ Test suite for ItemAPI """
    def test_create_new_item(self):
        """ Tests whether a user can create a new item based on a bucketlist_id """
        # create new bucketlist
        new_bucket_list = json.dumps(dict(
            bucketlist_name="Kenya"
        ))

        url = "/api/v1.0/bucketlists/"

        self.client.post(url, data=new_bucket_list, \
        content_type="application/json", headers=self.headers)

        new_item = json.dumps(dict(
            item_name="Go on a safari"
        ))

        url = "/api/v1.0/bucketlists/1/items/"

        response = self.client.post(url, data=new_item, \
        content_type="application/json", headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertTrue(data["item_name"] == "Go on a safari")
