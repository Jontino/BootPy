from bootpy import app, db
from bootpy.models import Relay, RelayEvent
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    db.create_all()
    print('Initialized the database')

@manager.command
def add_data():
    Relay.add_relay('Relay0', 4)
    Relay.add_relay('Relay1', 17)
    Relay.add_relay('Relay2', 27)
    Relay.add_relay('Relay3', 22)
    print('Default Relays added to database')

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
