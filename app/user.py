from flask import Flask
from app.models import BucketList, Item
from flask_restful import Api, Resource, reqparse
from app.db_setup import db

# Declare an instance Flask-Restful Api class
app = Flask(__name__)
api = Api(app)

class LoginAPI(Resource):
    """ Creates endpoints for LoginAPI """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email_address', type = str, required = True,
            help = 'No email address provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
            help = 'No password provided', location = 'json')            

    def post(self):
        """ Logs a user in """
        pass

class RegisterAPI(Resource):
        """ Creates endpoints for RegisterAPI """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True,
            help = 'No username provided', location = 'json')           
        self.reqparse.add_argument('email', type=inputs.regex(r"[^@]+@[^@]+\.[^@]+"), required=True,
                                   help="Invalid email format", location='json')
        self.reqparse.add_argument('password', type = str, required = True,
            help = 'No password provided', location = 'json')            

    def post(self):
        """ Register a user """
        pass
