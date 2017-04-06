from run_app import app, db

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    """ model for table users """
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True)
    email_address = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    def hash_this_pass(self, password):
        """ Creates a hash value from password passed """
        self.password_hash = pwd_context.encrypt(password)

class BucketList(db.Model):
    """ model for table bucketlists """
    __tablename__ = 'bucketlists'
    bucketlist_id = db.Column(db.Integer, primary_key = True)
    bucketlist_name = db.Column(db.String(64), index = True)
    created_by = created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    items = db.relationship('Item', backref='bucketlists', cascade='all,delete', passive_deletes=True)

class Item(db.Model):
    """ model for table items """
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.String(60), index = True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlists.bucketlist_id", ondelete="CASCADE"))
    done = db.Column(db.Boolean, default=False)

db.create_all(bind='__all__')