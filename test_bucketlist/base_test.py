import os
from flask_testing import TestCase


from run_app import app, db
from models import User, BucketList, Item

class BaseTestCase(TestCase):
    """ Initialize app and setup db resources """
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        """ Initialize resources for our tests """
        db.create_all()
        new_user = User(
            username='newguy',
            email_address="test@user.com"
        )
        new_user.hash_this_pass("thispass")
        db.session.add(new_user)
        db.session.commit()

    def tearDown(self):
        """ Clear resources after tests are run """
        db.session.remove()
        db.drop_all()
        os.remove('test.db')

