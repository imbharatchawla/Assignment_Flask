'''
This file contains all the routes for the app
'''

from audio_app import api
from audio_app.controllers.uploadController import Media, DeleteMedia
api.add_resource(Media, '/create/<audioType>', '/update/<audioType>/<audioID>', '/getmedia/<audioType>/', '/getmedia/<audioType>/<audioID>' )
api.add_resource(DeleteMedia, '/delete/<audioType>/<audioID>')