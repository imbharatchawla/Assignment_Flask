from flask import Flask, request, render_template, json, make_response
from flask_restful import Resource, Api, reqparse
from datetime import datetime
import os
import random
from audio_app import app, audio_db
from audio_app.services.mediaservice import MediaServices
import datetime
allowed_media_types = ['song', 'podcast', 'audiobook']

def check_validations(data, audioType):
    final_data = {}
    try:
        uploaded_date = data['uploaded_time'].split(' ')[0]
        uploaded_date = datetime.datetime.strptime(uploaded_date, '%Y-%m-%d')
        if str(uploaded_date).split(' ')[0] == str(datetime.date.today()):
            final_data['uploaded_time'] = data['uploaded_time']
        else:
            error_message = 'Date Cannot be Old or in Future!'
            return False, error_message
            
        try:
            if len(data['name']) <=100 and type(data['name'] is str):
                final_data['name'] = data['name']
        except:
            pass

        if data['duration'] > 0 and type(data['duration'] is int):
            final_data['duration'] = data['duration']

        final_data['id'] = data['id']
        if audioType == 'podcast':
            if data['host'] is None or data['host'] == '':
                error_message = 'Hostname cannot be blank'
                return False, error_message

            if len(data['host']) <= 100 and type(data['host'] is str):
                final_data['host'] = data['host']
            else:
                error_message = 'Too Long host name, must be under 100 characters!'
                return False, error_message
            if data['participants'] is None:
                error_message = 'Participant List cannot be empty'
                return False, error_message
            if data['participants'] != [] and len(data['participants']) <=10 and len(data['participants']) >=1:
                for participants_details in data['participants']:
                    if len(participants_details) <= 100:
                        pass
                
            elif data['participants'] == []:
                error_message = 'error in participant list'
                return False, error_message

            else:
                error_message = 'Must only contain 10 participants!'
                return False, error_message

            final_data['participants'] = data['participants']

        if audioType == 'audiobook':
            if len(data['title_of_the_audiobook']) <= 100 and len(data['title_of_the_audiobook']) >0:
                final_data['title_of_the_audiobook'] = data['title_of_the_audiobook']
                
            elif data['title_of_the_audiobook'] == '' or data['title_of_the_audiobook'] is None:
                error_msg = 'title_of_the_audiobook is blank'
                return False, error_msg
            else:
                error_msg = 'title_of_the_audiobook (should be less than 100 characters)'
                return False, error_msg
                
  
            if len(data['author_of_the_title']) <= 100 and len(data['author_of_the_title']) > 0:
                final_data['author_of_the_title'] = data['author_of_the_title']
            elif data['author_of_the_title'] == '' or data['author_of_the_title'] is None:
                error_msg = 'author_of_the_title is blank'
                return False, error_msg
            else:
                error_msg = 'author_of_the_title is too large (should be less than 100 characters)'
                return False, error_msg
   
            if len(data['narrator']) <= 100 and len(data['narrator']) > 0:
                final_data['narrator'] = data['narrator']
            elif data['narrator'] == '' or data['narrator'] is None:
                error_msg = 'narrator is blank'
                return False, error_msg
            else:
                error_msg = 'narrator name is too large (should be less than 100 characters)'
                return False, error_msg

        return True, final_data 
             
    except Exception as e:
        return {'error': str(e)}

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
        if audioType.lower() == 'song' or audioType.lower() == 'podcast':
            parser.add_argument('name', type=str, help='Name can not be blank', required=True)
        parser.add_argument('duration', type=int, help='Duration can not be blank', required=True)
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('uploaded_time', required=True)

        if audioType.lower() == 'podcast':
            parser.add_argument('host', type=str, required=True)
            parser.add_argument('participants', type=str, action= 'append', required=False)

        elif audioType.lower() == 'audiobook':
            parser.add_argument('title_of_the_audiobook', type=str, required=True)
            parser.add_argument('author_of_the_title', type=str, required=True)
            parser.add_argument('narrator', type=str, required=True)

        elif audioType.lower() not in allowed_media_types:
            return {"error": "Please enter valid media type"}

        args = parser.parse_args()
        validated_data = check_validations(dict(args), audioType)
        if validated_data[0]:
            app.logger.debug("CreateMedia::POST::params::{}".format(validated_data[1]))
            result = MediaServices().uploadMedia(audioType, validated_data[1])
            return result
        else:
            return {'error': validated_data[1]}
    
    def put(self, audioType, audioID):
        data = {}
        parser = reqparse.RequestParser()
        if audioType.lower() == 'song' or audioType.lower() == 'podcast':
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
        validated_data = check_validations(dict(args), audioType)
        if validated_data[0]:
            result = MediaServices().updateMedia(audioType, int(audioID), validated_data[1])
            return result
        else:
            return {'error': validated_data[1]}


class DeleteMedia(Resource):
    def post(self, audioType, audioID):
        if audioID == None or audioType == None:
            return {"Message": "Please provide valid media type and ID"}
        else:
            result = MediaServices().deleteMedia(audioType, int(audioID))

        return result

