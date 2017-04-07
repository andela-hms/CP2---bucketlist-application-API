from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal,inputs

from models import User
from run_app import app, db

# Declare Blueprint
user_blueprint = Blueprint('user_endpoint', __name__)
auth_api = Api(user_blueprint)

user_fields = { 'user_id': fields.Integer,
                        'username': fields.String,
                        'email_address': fields.String,
                        'password_hash': fields.String
}

class LoginAPI(Resource):
    """ Creates endpoints for LoginAPI """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type = str, required=True, help = 'No email address provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
            help = 'No password provided', location = 'json')            

    def post(self):
        """ Logs a user in """
        args = self.reqparse.parse_args()

        # fetch user data
        check_user = User.query.filter_by(email_address=args['email']).first()

        try:
            if check_user:
                if check_user.verify_pass(args['password']):
                    give_token = check_user.generate_auth_token()

                    json_response = {
                        'message': 'Login Successful',
                        'auth_token': give_token.decode()
                    }
                    return json_response, 200
                
                else:
                    json_response = {
                        'error': 'Invalid Password'
                    }
                    return json_response, 401
            else:
                json_response = {
                        'error': 'User with email {} does not exist'.format(args['email'])
                    }
                return json_response, 404
        except:
            json_response = {
                        'error': 'Login Failed'
                    }
            return json_response, 500


class RegisterAPI(Resource):

    """ Creates endpoints for RegisterAPI """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True, help = 'No username provided', location = 'json')           
        self.reqparse.add_argument('email', type=inputs.regex(r"[^@]+@[^@]+\.[^@]+"), required=True, help="Invalid email format", location='json')
        self.reqparse.add_argument('password', type = str, required = True, help = 'No password provided', location = 'json')
        super(RegisterAPI, self).__init__()

    def post(self):
        """ Registers a user """

        args = self.reqparse.parse_args()

        # Check whether user already exists
        check_user = User.query.filter_by(email_address=args['email']).first()

        if not check_user:
            try:
                check_user = User(username=args['username'], email_address=args['email'], password_hash=args['password'])
                # hash password before saving to db
                check_user.hash_this_pass(args['password'])

                # add user to db
                db.session.add(check_user)
                db.session.commit()

                # generate auth token
                token = check_user.generate_auth_token(check_user.user_id)

                # message on successful registration
                json_response = {
                    'message' : 'Registration successful',
                    'token' : 'token.decode()'
                }
                
                return json_response, 201

            except:
                json_response = {
                    'message' : 'Unable to register new user: {}'.format(args['username'])
                }

                return json_response, 400
        else:
            # user exists
            json_response = {
                    'message' : 'User already exists'
                }

            return json_response, 409

auth_api.add_resource(LoginAPI, '/auth/login/', endpoint='login')
auth_api.add_resource(RegisterAPI, '/auth/register/', endpoint='register')

