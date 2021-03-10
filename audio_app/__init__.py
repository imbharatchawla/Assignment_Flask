from flask import Flask, make_response, json, g, request, jsonify, redirect
from flask_restful import Resource, Api, reqparse
import datetime
import time
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config')
mongo_client = MongoClient(app.config['MONGOALCHEMY_SERVER'], app.config['MONGOALCHEMY_PORT'])
audio_db = mongo_client[app.config['MONGOALCHEMY_DATABASE']]

api = Api(app)
import audio_app.routes.routes