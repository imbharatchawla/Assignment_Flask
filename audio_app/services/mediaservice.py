from flask import Flask, request, render_template, json, make_response
from flask_restful import Resource, Api, reqparse
from datetime import datetime
import os
import random
from bson import json_util, ObjectId
from audio_app import app, audio_db
class MediaServices:

    
    def getMedia(self, audioType, audioID=None):
        if audioType == 'song':
            if audioID is not None:
                print('here')
                find_specific_media = audio_db.Song.find_one({"id": int(audioID)})
                return json.loads(json_util.dumps(find_specific_media))
            else:
                all_media = []
                find_all_media = audio_db.Song.find({})
                for all in find_all_media:
                    all_media.append(all)
                return json.loads(json_util.dumps(all_media))

    def uploadMedia(self, audioType, data):
        if audioType.lower() == 'song':
            find_same_audio = audio_db.Song.find_one({"id": data['id']})
            if find_same_audio:
                return {"message": "Duplicate Media with same ID found" }
            result = audio_db.Song.insert(data)
        elif audioType.lower() == 'podcast':
            find_same_audio = audio_db.Podcast.find_one({"id": data['id']})
            if find_same_audio:
                return {"message": "Duplicate Media with same ID found" }
            result = audio_db.Podcast.insert(data)
        elif audioType.lower() == 'audiobook':
            find_same_audio = audio_db.Audiobook.find_one({"id": data['id']})
            if find_same_audio:
                return {"message": "Duplicate Media with same ID found" }
            result = audio_db.Audiobook.insert(data)

        if result:
            return {"message": "Success"}
        else:
            return {"error": "Some error occured"}
    
    
    def deleteMedia(self, audioType, audioID):
        app.logger.debug("DeleteMedia")
        if audioType.lower() == 'song':
            find_audio = audio_db.Song.find_one_and_delete({"id": audioID})
            if find_audio:
                return {"message": "Media with ID {} deleted successfully" .format(audioID)}
        elif audioType.lower() == 'podcast':
            find_audio = audio_db.Podcast.find_one_and_delete({"id": audioID})
            print(find_audio, type(audioID))
            if find_audio:
                return {"message": "Media with ID {} deleted successfully" .format(audioID)}
        elif audioType.lower() == 'audiobook':
            find_audio = audio_db.Audiobook.find_one_and_delete({"id": audioID})
            if find_audio:
                return {"message": "Media with ID {} deleted successfully" .format(audioID)}
        else:
            return {"message": "Something went wrong"}
    
    def updateMedia(self, audioType, audioID, data):
        if audioType.lower() == 'song':
            find_same_audio = audio_db.Song.find_one_and_update({"id": audioID}, {'$set': data})
            if find_same_audio:
                return {"message": "Media with ID {} updated" .format(audioID) }
            else:
                return {"message": "Nothing Found" }
        elif audioType.lower() == 'podcast':
            find_same_audio = audio_db.Podcast.find_one_and_update({"id": audioID}, {'$set': data})
            if find_same_audio:
                return {"message": "Media with ID {} updated" .format(audioID) }
            else:
                return {"message": "Nothing Found" }
        elif audioType.lower() == 'audiobook':
            find_same_audio = audio_db.Audiobook.find_one_and_update({"id": audioID}, {'$set': data})
            if find_same_audio:
                return {"message": "Media with ID {} updated" .format(audioID) }
            else:
                return {"message": "Nothing Found" }

        else:
            return {"error": "Some error occured"}