import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TMP_DIR = '/tmp/'
DEBUG = True
LOG_FILE = '/var/log/oktested/oktested.log'
LOG_LEVEL = 'DEBUG'

MONGO_SERVER = 'localhost'
MONGO_USER = None
MONGO_PASSWORD = None
MONGO_DATABASE = 'Audio'
MONGO_PORT = 27017
MONGO_COLLECTION_SONG = 'Song'
MONGO_COLLECTION_PODCAST = 'Podcast'
MONGO_COLLECTION_AUDIOBOOK = 'Audiobook'

allowed_media_types = ['song' 'podcast', 'audiobook']
