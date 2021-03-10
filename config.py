import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TMP_DIR = '/tmp/'
DEBUG = True
LOG_FILE = '/var/log/oktested/oktested.log'
LOG_LEVEL = 'DEBUG'

#https://pythonhosted.org/Flask-MongoAlchemy/
MONGOALCHEMY_SERVER = 'localhost'
MONGOALCHEMY_USER = None
MONGOALCHEMY_PASSWORD = None
MONGOALCHEMY_DATABASE = 'Audio'
MONGOALCHEMY_PORT = 27017
MONGOALCHEMY_COLLECTION_SONG = 'Song'
MONGOALCHEMY_COLLECTION_PODCAST = 'Podcast'
MONGOALCHEMY_COLLECTION_AUDIOBOOK = 'Audiobook'

allowed_media_types = ['song' 'podcast', 'audiobook']
