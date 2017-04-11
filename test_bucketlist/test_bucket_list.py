import json
from base_test import BaseTestCase

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

    def test_get_bucket_lists(self):
        """ Test if user can get a list of bucketlists saved in the database """

        # new bucketlist
        new_bucket_list = json.dumps(dict(
            bucketlist_name="Asia"
        ))
        self.client.post(URL, data=new_bucket_list, \
        content_type="application/json", headers=self.headers)

        # get bucketlists
        response = self.client.get(URL, \
        content_type="application/json", headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["message"]["total"] == 1)

    def test_duplicates(self):
        """
        Tests behaviour of endepoint when duplicate bucketlists are created
        """
        new_bucket_list = json.dumps(dict(
            bucketlist_name="Asia"
        ))
        self.client.post(URL, data=new_bucket_list, \
        content_type="application/json", headers=self.headers)

        # create similar bucketlist
        response = self.client.post(URL, data=new_bucket_list, \
        content_type="application/json", headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertTrue(data["error"] == "bucketlist_name Asia already exists")

        