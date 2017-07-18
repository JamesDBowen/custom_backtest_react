from flask import Flask
from flask_mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
import settings
from flask.ext.cors import CORS
import flask_restless

app = Flask(__name__)



db = SQLAlchemy(app)
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
bcrypt = Bcrypt(app)
mail = Mail(app)
CORS(app)

app.secret_key = settings.SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = True
app.config['TESTING'] = False

app.config['MAIL_SERVER'] = settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
app.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
app.config['DEFAULT_MAIL_SENDER'] = settings.DEFAULT_MAIL_SENDER

from views import mod as viewsModule
from admin import mod as adminModule


#from views import mod as restModule
#from deanumber import mod as deanumberModule
#from auth import mod as authModule
#from dailymed import mod as dailymedModule
#from dnb import mod as dnbModule
#from shortage import mod as shortageModule
app.register_blueprint(viewsModule)
app.register_blueprint(adminModule)
