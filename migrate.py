import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from db_setup import app, db


app.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def create():
    """ Manually creates tables in the database """
    db.create_all()


@manager.command
def drop():
    """ Manually drops all tables that exist in the database """
    db.drop_all()

if __name__ == '__main__':
    manager.run()