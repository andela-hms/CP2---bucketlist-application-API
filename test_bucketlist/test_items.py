import json
from base_test import BaseTestCase

URL = "/api/v1.0/bucketlists/"

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

    def test_non_existent_bucketlist_id(self):
        """ Test behaviour if endpoint when user passes an invalid bucketlist_id """
        url = "/api/v1.0/bucketlists/100/items/"
        new_item = json.dumps(dict(
            item_name="Go on a safari"
        ))

        response = self.client.post(url, data=new_item, \
        content_type="application/json", headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertTrue(data["error"] == "Bucketlist_id 100 does not exists")

    def test_non_existent_item_id(self):
        """ Test whether itemAPI checks for invalid ids when a user wants to update an Item """
        # create bucketlist
        new_bucket_list = json.dumps(dict(
            bucketlist_name="Asia"
        ))
        self.client.post(URL, data=new_bucket_list, \
        content_type="application/json", headers=self.headers)

        url = "/api/v1.0/bucketlists/1/items/25"
        new_item = json.dumps(dict(
            item_name="Go for zip linning"
        ))

        response = self.client.put(url, data=new_item, \
        content_type="application/json", headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertTrue(data["error"] == "item_id does not exists")
