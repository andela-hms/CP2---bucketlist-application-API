from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with

from models import BucketList, Item
from run_app import app, db


# Declare the Blueprint app
blueprint = Blueprint('bucket_list', __name__)
api = Api(blueprint)

bucket_list_fields = { 'bucketlist_id' : fields.Integer,
                        'bucketlist_name': fields.String,
                        'created_by' : fields.Integer,
                        'date_created': fields.DateTime,
                        'date_modified': fields.DateTime
}

item_fields = { 'item_id' : fields.Integer,
                        'item_name': fields.String,
                        'created_by' : fields.Integer,
                        'date_created': fields.DateTime,
                        'date_modified': fields.DateTime,
                        'bucketlist_id' : fields.Integer,
                        'done': fields.Boolean
}

class BucketListAPI(Resource):
    """ Creates endpoints for BucketListAPI """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('bucketlist_name', type = str, required = True,
            help = 'No BucketList name provided', location = 'json')
        super(BucketListAPI, self).__init__()
    
    @marshal_with(bucket_list_fields, envelope='Bucketlists')
    def get(self, id=None):

        """ List all the created bucket lists and single ones too """
        bucketlists = BucketList.query.all()

        return bucketlists

    def post(self):
        """ Create a new bucket list """
        args = self.reqparse.parse_args()
        name = args['bucketlist_name']

        check_duplicate = BucketList.query.filter_by(bucketlist_name=name).first()

        if check_duplicate:
            return {'error': 'bucketlist_name {} already exists'.format(name)}
        
        new_bucketlist = BucketList(bucketlist_name=name)
        db.session.add(new_bucketlist)
        db.session.commit()

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

api.add_resource(BucketListAPI, '/bucketlists/', endpoint = 'bucketlists')