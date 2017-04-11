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
                bucketlists = BucketList.query.filter_by(created_by=g.user.user_id) \
                .paginate(page, limit, False)

            if not bucketlists:
                return {'message': 'bucketlists not found'}, 400

            if bucketlists.has_prev:
                prev_page = request.url_root + 'api/v1.0/bucketlists/' +'?page='\
                 + str(page-1) + '&limit=' + str(limit)
            else:
                prev_page = 'None'

            if bucketlists.has_next:
                next_page = request.url_root + 'api/v1.0/bucketlists/' + '?page='\
                 + str(page+1) + '&limit=' + str(limit)
            else:
                next_page = 'None'

            return {
                'message': {
                    'next_page':next_page,
                    'prev_page': prev_page,
                    'total_pages': bucketlists.pages},
                'bucketlists': marshal(bucketlists.items, bucket_list_fields)
            }, 200


    def post(self):
        """ Create a new bucket list """
        args = self.reqparse.parse_args()
        name = args['bucketlist_name']

        check_duplicate = BucketList.query.filter_by(bucketlist_name=name, \
        created_by=g.user.user_id).first()

        if check_duplicate:
            return {'error': 'bucketlist_name {} already exists'.format(name)}, 403

        new_bucketlist = BucketList(bucketlist_name=name, created_by=g.user.user_id)
        db.session.add(new_bucketlist)
        db.session.commit()

        return {
            'message' : 'New bucketlist created successfully',
            'bucketlist': marshal(new_bucketlist, bucket_list_fields)
        }, 201

    def put(self, id):
        """ Update a bucket list """
        this_bucket_list = BucketList.query.filter_by(bucketlist_id=id, \
        created_by=g.user.user_id).first()
        if not this_bucket_list:
            return {'error': 'bucketlist with id {} does not exists'.format(id)}, 400
        args = self.reqparse.parse_args()
        name = args['bucketlist_name']

        update_bucketlist = BucketList.query.filter_by(bucketlist_id=id).first()
        update_bucketlist.bucketlist_name = name
        db.session.commit()

        return {
            'message' : 'Update was successfull',
            'bucketlist': marshal(update_bucketlist, bucket_list_fields)
        }, 201

    def delete(self, id):
        """ Delete a single bucket list """
        this_bucket_list = BucketList.query.filter_by(bucketlist_id=id, \
        created_by=g.user.user_id).first()
        if not this_bucket_list:
            return {'error': 'bucketlist with id {} does not exists'.format(id)}, 400

        db.session.delete(this_bucket_list)
        db.session.commit()

        return {'message': 'bucketlist with id {} has been deleted'.format(id)}, 202

class ItemAPI(Resource):
    """ Creates endpoints for ItemAPI """
    decorators = [auth_user.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type=str, \
        help='No Item name provided', location='json')
        self.reqparse.add_argument('done', default=False, type=bool, location='json')
        super(ItemAPI, self).__init__()

    def get(self, itemid=None):
        """ Fetches all the created items """
        if itemid:
            this_item = Item.query.filter_by(Item_id=itemid).first()
            return marshal(this_item, item_fields), 200

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
                items = Item.query.filter(Item.item_name.like('%'+query+'%') \
                ).paginate(page, limit, False)
            else:
                items = Item.query.filter().paginate(page, limit, False)

            if not items:
                return {'message': 'items not found'}, 400

            if items.has_prev:
                prev_page = request.url_root + 'api/v1.0/bucketlists/items/' +'?page='\
                 + str(page-1) + '&limit=' + str(limit)
            else:
                prev_page = 'None'

            if items.has_next:
                next_page = request.url_root + 'api/v1.0/bucketlists/items/' + '?page='\
                 + str(page+1) + '&limit=' + str(limit)
            else:
                next_page = 'None'

            return {
                'message': {
                    'next_page':next_page,
                    'prev_page': prev_page,
                    'total_pages': items.pages},
                'items': marshal(items.items, item_fields)
            }, 200

    def post(self, bucketlist_id):
        """ Create a new item in bucket list based on the bucketlist_id """
        args = self.reqparse.parse_args()
        name = args['item_name']
        bucketlist_exists = BucketList.query.filter_by(bucketlist_id=bucketlist_id, \
        created_by=g.user.user_id).first()

        if not bucketlist_exists:
            return {'error': 'Bucketlist_id {} does not exists'.format(bucketlist_id)}, 400

        new_item = Item(item_name=name, bucketlist_id=bucketlist_id)
        db.session.add(new_item)
        db.session.commit()

        return {
            'message' : 'New bucketlist item created successfully',
            'bucketlist': marshal(new_item, item_fields)
        }, 201

    def put(self, bucketlist_id, item_id):
        """ Update a bucket list item """
        bucketlist_exists = BucketList.query.filter_by(bucketlist_id=bucketlist_id).first()

        if bucketlist_exists:
            item_exists = Item.query.filter_by(item_id=item_id).first()

            if item_exists:
                args = self.reqparse.parse_args()
                name = args['item_name']
                done = args['done']

                if name:
                    item_exists.item_name = name

                if done in [True, False]:
                    item_exists.done = done

                db.session.commit()

                return marshal(item_exists, item_fields)

            else:
                return {'error': 'item_id does not exists'}, 400

        else:
            return {'error': 'bucketlist_id does not exists'}, 400

    def delete(self, bucketlist_id, item_id):
        """ Delete an item in a bucket list """
        bucketlist_exists = BucketList.query.filter_by(bucketlist_id=bucketlist_id).first()
        item_exists = Item.query.filter_by(item_id=item_id).first()

        if not (bucketlist_exists or item_exists):
            return {'error': 'bucketlist_id or item_id does not exists'}, 400

        db.session.delete(item_exists)
        db.session.commit()

        return {'message': 'Item with id {} has been deleted'.format(item_id)}, 202

api.add_resource(BucketListAPI, '/api/v1.0/bucketlists/<int:id>/', \
'/api/v1.0/bucketlists/', endpoint='bucketlists')
api.add_resource(ItemAPI, '/api/v1.0/bucketlists/<int:bucketlist_id>/items/', \
'/api/v1.0/bucketlists/<int:bucketlist_id>/items/<int:item_id>', \
'/api/v1.0/bucketlists/items/', endpoint='items')
