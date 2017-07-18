from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import settings
from app import views, models
import csv, random
from datetime import datetime, timedelta, date
    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)
from app.models import *
migrate = Migrate(app, db, directory='app/migrations')

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
