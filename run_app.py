import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initialize the app
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)

from app.bucket_list import blueprint
app.register_blueprint(blueprint)

from app.user import user_blueprint
app.register_blueprint(user_blueprint)

if __name__ == '__main__':
    app.run()
    