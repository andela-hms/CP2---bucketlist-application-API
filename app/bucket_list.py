from flask import Flask
from app.models import BucketList, Item
from flask_restful import Api, Resource, reqparse
from app.db_setup import db

# Declare an instance Flask-Restful Api class
app = Flask(__name__)
api = Api(app)

class BucketListAPI(Resource):
    """ Creates endpoints for BucketListAPI """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('bucketlist_name', type = str, required = True,
            help = 'No BucketList name provided', location = 'json')
        super(BucketListAPI, self).__init__()

    def get(self, id=None):
        """ List all the created bucket lists and single ones too """
        pass

    def post(self):
        """ Create a new bucket list """
        pass

    def put(self, id):
        """ Update a bucket list """
        pass

    def delete(self, id):
        """ Delete a single bucket list """
        pass

class ItemAPI(Resource):
    """ Creates endpoints for ItemAPI """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(ItemAPI, self).__init__()

    def post(self, bucketlist_id):
        """ Create a new item in bucket list based on the bucketlist_id """
        pass

    def put(self, bucketlist_id, item_id):
        """ Update a bucket list item """
        pass

    def delete(self, bucketlist_id, item_id):
        """ Delete an item in a bucket list """
        pass