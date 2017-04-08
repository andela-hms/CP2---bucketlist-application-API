import os
from flask_testing import TestCase


from run_app import app, db
from models import User, BucketList, Item

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        new_user = User(
            username='testuser',
            email_address="test@user.com",
        )
        new_user.hash_this_pass("thispass")
        db.session.add(new_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('test.db')


