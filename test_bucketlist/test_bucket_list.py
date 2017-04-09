import json
from base_test import BaseTestCase

URL = "/bucketlists/"
class BucketListestCase(BaseTestCase):
    def test_create_bucket_list(self):
        """ Tests whether a user can create a bucketlist """
        data = json.dumps(dict(
                bucketlist_name="Kenya"
        ))

        headers = json.dumps({"Content-Type":"application/json","Accept":"application/json"})
        response = self.client.post(URL, data=data, content_type="application/json")
        self.assertIn(" ",response.data.decode())

        def 