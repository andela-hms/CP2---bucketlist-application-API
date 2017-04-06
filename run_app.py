import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the app
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app.bucket_list import blueprint
# register blueprint as part of the app
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run()