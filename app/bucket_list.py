from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal

from models import BucketList, Item
from run_app import app, db


# Declare the Blueprint app
blueprint = Blueprint('bucket_list', __name__)
api = Api(blueprint)

item_fields = { 'item_id' : fields.Integer,
                        'item_name': fields.String,
                        'created_by' : fields.Integer,
                        'date_created': fields.DateTime,
                        'date_modified': fields.DateTime,
                        'bucketlist_id' : fields.Integer,
                        'done': fields.Boolean
}

bucket_list_fields = { 'bucketlist_id' : fields.Integer,
                        'bucketlist_name': fields.String,
                        'created_by' : fields.Integer,
                        'items': fields.Nested(item_fields),
                        'date_created': fields.DateTime,
                        'date_modified': fields.DateTime
}

class BucketListAPI(Resource):
    """ Creates endpoints for BucketListAPI """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('bucketlist_name', type = str, required = True,
            help = 'No BucketList name provided', location = 'json')
        super(BucketListAPI, self).__init__()
    
    def get(self, id=None):

        """ List all the created bucket lists and single ones too """
        if id:
            this_bucket_list = BucketList.query.filter_by(bucketlist_id=id).first()
            return this_bucket_list
        else:
            bucketlists = BucketList.query.all()

            return marshal(bucketlists, bucket_list_fields)

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

        return marshal(new_bucketlist, bucket_list_fields)

    def put(self, id):
        """ Update a bucket list """
        this_bucket_list = BucketList.query.filter_by(bucketlist_id=id).first()
        if not this_bucket_list:
            return {'error': 'bucketlist with id {} does not exists'.format(id)}
        args = self.reqparse.parse_args()
        name = args['bucketlist_name']

        update_bucketlist = BucketList.query.filter_by(bucketlist_id=id).first()
        update_bucketlist.bucketlist_name = name
        db.session.commit()

        return marshal(update_bucketlist, bucket_list_fields)

    def delete(self, id):
        """ Delete a single bucket list """
        this_bucket_list = BucketList.query.filter_by(bucketlist_id=id).first()
        if not this_bucket_list:
            return {'error': 'bucketlist with id {} does not exists'.format(id)}

        db.session.delete(this_bucket_list)
        db.session.commit()

        return {'error': 'bucketlist with id {} has been deleted'.format(id)}
        
class ItemAPI(Resource):
    """ Creates endpoints for ItemAPI """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type = str, required = True,
            help = 'No Item name provided', location = 'json')
        super(ItemAPI, self).__init__()

    def post(self, bucketlist_id):
        """ Create a new item in bucket list based on the bucketlist_id """
        args = self.reqparse.parse_args()
        name = args['item_name']
        bucketlist_exists = BucketList.query.filter_by(bucketlist_id=bucketlist_id).first()

        if not bucketlist_exists:
            return {'error': 'bucketlist_id {} does not exists'.format(bucketlist_id)}

        new_item = Item(item_name=name, bucketlist_id=bucketlist_id)
        db.session.add(new_item)
        db.session.commit()

    def put(self, bucketlist_id, item_id):
        """ Update a bucket list item """
        pass

    def delete(self, bucketlist_id, item_id):
        """ Delete an item in a bucket list """
        pass

api.add_resource(BucketListAPI, '/bucketlists/', '/bucketlists/<int:id>/', endpoint='bucketlists')
api.add_resource(ItemAPI, '/bucketlists/<int:bucketlist_id>/items/', endpoint='items')
