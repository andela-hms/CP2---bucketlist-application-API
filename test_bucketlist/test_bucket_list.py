import os
import json
from run_app import app, db

from base_test import BaseTestCase
from models import User, BucketList, Item

URL = "/api/v1.0/bucketlists/"

class BucketListTestCase(BaseTestCase):
    """ Test suite for BucketList API """
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

    def test_update_bucketlist(self):
        """ Tests whether a user can create a new bucketlist """
        edit_bucket_list = json.dumps(dict(
            bucketlist_name="Silicon Savannah"
        ))

        url = "/api/v1.0/bucketlists/1/"

        response = self.client.put(url, data=edit_bucket_list, \
        content_type="application/json", headers=self.headers)
        self.assertEqual(response.status_code, 200)

