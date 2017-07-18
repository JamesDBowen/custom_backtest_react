import os
_basedir = os.path.abspath(os.path.dirname(__file__))

# Flask Secret Key
SECRET_KEY = '\xd5\xb2?\x8fPS\xdc\xf6#\t\x9b\x15\x93;@\x05\x81g\xc9\x16\xabO)\xca'

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = 'mysql://chicken:chicken@localhost/chicken'


# Flask-Mail configuration
MAIL_SERVER = 'email-smtp.us-west-2.amazonaws.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
QUANDL_API_KEY = "E_Yw5tEUPzAXsD2psxad"
MAIL_USERNAME = 'AKIAIIY3XT5IUA4DNICQ'
MAIL_PASSWORD = 'As5mOmM8T1daUA4yqErRvY4k/yfLL7XSVG9/IBM4wX7O'
DEFAULT_MAIL_SENDER = 'info@chicken.com'
DEFAULT_MAIL_NAME = 'ChickenAdmin'


DAILYMED_API_URL = 'http://dailymed.nlm.nih.gov/dailymed/services/v2'

BLOOMAPI_URL = 'http://www.bloomapi.com/api'
BLOOMAPI_SECRET = 'IDWxogY5naWnSnPW3WjwzTaxSbj7IFCc'

ACCEPTED_IMAGE_MIMETYPES = ('image/jpeg', 'image/png')
MAX_IMAGE_HEIGHT = 1024
MAX_IMAGE_WIDTH = 1024

DEBUG = True

"""
Because the data in each CloudSearch domain necessarily reflects a particular
database, these settings have to be set individually in local_settings.py for
each server.
"""
CLOUDSEARCH_LISTINGS_DOMAIN = None
CLOUDSEARCH_LISTINGS_HOST = None

try:
    from local_settings import *
except ImportError:
    pass
