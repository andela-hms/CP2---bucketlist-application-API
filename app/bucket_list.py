from flask import Flask, Blueprint, g, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPTokenAuth
from models import BucketList, Item, User
from run_app import app, db

# Declare Blueprint
blueprint = Blueprint('bucket_list', __name__)
api = Api(blueprint)

auth_user = HTTPTokenAuth(scheme="Token")

@auth_user.verify_token
def verify_token(token):
    """ Validate token passed """
    # verify user token
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

item_fields = {
    'item_id' : fields.Integer,
    'item_name': fields.String,
    'created_by' : fields.Integer,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'bucketlist_id' : fields.Integer,
    'done': fields.Boolean
}

bucket_list_fields = {
    'bucketlist_id' : fields.Integer,
    'bucketlist_name': fields.String,
    'created_by' : fields.Integer,
    'items': fields.Nested(item_fields),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}

class BucketListAPI(Resource):
    """ Creates endpoints for BucketListAPI """

    decorators = [auth_user.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('bucketlist_name', type=str, \
        required=True, help='No BucketList name provided', location='json')
        super(BucketListAPI, self).__init__()

    def get(self, id=None):
        """ List all the created bucket lists and single ones too """
        if id:
            this_bucket_list = BucketList.query.filter_by(bucketlist_id=id, \
            created_by=g.user.user_id).first()
            return marshal(this_bucket_list, bucket_list_fields), 200

        else:

            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('q', type=str, location='args')
            self.reqparse.add_argument('limit', type=int, location='args', default=20)
            self.reqparse.add_argument('page', type=int, location='args', default=1)

            args = self.reqparse.parse_args()
            query = args['q']
            limit = args['limit']
            page = args['page']

            if query:
                bucketlists = BucketList.query.filter(BucketList.bucketlist_name.like('%'+query+'%'), \
                BucketList.created_by == g.user.user_id).paginate(page, limit, False)
            else:
                bucketlists = BucketList.query.filter_by(created_by=g.user.user_id).paginate(page, limit, False)

            if not bucketlists:
                return {'message': 'bucketlists not found'}, 404

            if bucketlists.has_prev:
                prev_page = request.url + '?page=' + str(page - 1) + '&limit=' + str(limit)
            else:
                prev_page = 'None'

            if bucketlists.has_next:
                next_page = request.url + '?page=' + str(page + 1) + '&limit=' + str(limit)
            else:
                next_page = 'None'

            return {
                'message': {
                    'next_page':next_page,
                    'prev_page': prev_page,
                    'total': bucketlists.pages},
                'bucketlists': marshal(bucketlists.items, bucket_list_fields)
            }, 200


    def post(self):
        """ Create a new bucket list """
        args = self.reqparse.parse_args()
        name = args['bucketlist_name']

        check_duplicate = BucketList.query.filter_by(bucketlist_name=name).first()

        if check_duplicate:
            return {'error': 'bucketlist_name {} already exists'.format(name)}

        new_bucketlist = BucketList(bucketlist_name=name, created_by=g.user.user_id)
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

        return {'message': 'bucketlist with id {} has been deleted'.format(id)}

class ItemAPI(Resource):
    """ Creates endpoints for ItemAPI """
    decorators = [auth_user.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type=str, required=True, \
        help='No Item name provided', location='json')
        super(ItemAPI, self).__init__()

    def post(self, bucketlist_id):
        """ Create a new item in bucket list based on the bucketlist_id """
        args = self.reqparse.parse_args()
        name = args['item_name']
        bucketlist_exists = BucketList.query.filter_by(bucketlist_id=bucketlist_id).first()

        if not bucketlist_exists:
            return {'error': 'Bucketlist_id {} does not exists'.format(bucketlist_id)}

        new_item = Item(item_name=name, bucketlist_id=bucketlist_id)
        db.session.add(new_item)
        db.session.commit()

        return marshal(new_item, item_fields)

    def put(self, bucketlist_id, item_id):
        """ Update a bucket list item """
        bucketlist_exists = BucketList.query.filter_by(bucketlist_id=bucketlist_id).first()
        item_exists = Item.query.filter_by(item_id=item_id).first()

        if not (bucketlist_exists or item_exists):
            return {'error': 'bucketlist_id or item_id does not exists'}

        args = self.reqparse.parse_args()
        name = args['item_name']

        update_item = Item.query.filter_by(item_id=item_id).first()
        update_item.item_name = name
        db.session.commit()

        return marshal(update_item, item_fields)

    def delete(self, bucketlist_id, item_id):
        """ Delete an item in a bucket list """
        bucketlist_exists = BucketList.query.filter_by(bucketlist_id=bucketlist_id).first()
        item_exists = Item.query.filter_by(item_id=item_id).first()

        if not (bucketlist_exists or item_exists):
            return {'error': 'bucketlist_id or item_id does not exists'}

        db.session.delete(item_exists)
        db.session.commit()

        return {'message': 'Item with id {} has been deleted'.format(item_id)}

api.add_resource(BucketListAPI, '/bucketlists/<int:id>/', '/bucketlists/', endpoint='bucketlists')
api.add_resource(ItemAPI, '/bucketlists/<int:bucketlist_id>/items/', \
'/bucketlists/<int:bucketlist_id>/items/<int:item_id>', endpoint='items')
