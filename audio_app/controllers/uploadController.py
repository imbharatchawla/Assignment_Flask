from flask import Flask, request, render_template, json, make_response
from flask_restful import Resource, Api, reqparse
from datetime import datetime
import os
import random
from audio_app import app, audio_db
from audio_app.services.mediaservice import MediaServices
allowed_media_types = ['song', 'podcast', 'audiobook']

class Media(Resource):

    def get(self, audioType, audioID=None):
        if audioType is None:
            return {"Error": "Please enter valid values"}
        else:
            result = MediaServices().getMedia(audioType, audioID)
            return result
    def post(self, audioType):
        data = {}
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name can not be blank', required=True)
        parser.add_argument('duration', type=int, help='Duration can not be blank', required=True)
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('uploaded_time', type=str, required=True)

        if audioType.lower() == 'podcast':
            parser.add_argument('host', type=str, required=True)
            parser.add_argument('participants', type=str, required=False)

        elif audioType.lower() == 'audiobook':
            parser.add_argument('title_of_the_audiobook', type=str, required=True)
            parser.add_argument('author_of_the_title', type=str, required=True)
            parser.add_argument('narrator', type=str, required=True)

        elif audioType.lower() not in allowed_media_types:
            return {"error": "Please enter valid media type"}

        args = parser.parse_args()
        app.logger.debug("CreateMedia::POST::params::{}".format(args))
        data = dict(args)
        result = MediaServices().uploadMedia(audioType, data)
        return result
    
    def put(self, audioType, audioID):
        data = {}
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name can not be blank', required=True)
        parser.add_argument('duration', type=int, help='Duration can not be blank', required=True)
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('uploaded_time', type=str, required=True)

        if audioType.lower() == 'podcast':
            parser.add_argument('host', type=str, required=True)
            parser.add_argument('participants', type=str, required=False)

        elif audioType.lower() == 'audiobook':
            parser.add_argument('title_of_the_audiobook', type=str, required=True)
            parser.add_argument('author_of_the_title', type=str, required=True)
            parser.add_argument('narrator', type=str, required=True)

        elif audioType.lower() not in allowed_media_types or audioID is None:
            return {"error": "Please enter valid media type or audio ID"}

        args = parser.parse_args()
        app.logger.debug("CreateMedia::POST::params::{}".format(args))
        data = dict(args)
        result = MediaServices().updateMedia(audioType, int(audioID), data)
        return result


class DeleteMedia(Resource):
    def post(self, audioType, audioID):
        if audioID == None or audioType == None:
            return {"Message": "Please provide valid media type and ID"}
        else:
            result = MediaServices().deleteMedia(audioType, int(audioID))

        return result

