from flask import Flask, make_response, json, g, request, jsonify, redirect
from flask_restful import Resource, Api, reqparse
import datetime
import time
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config')
mongo_client = MongoClient(app.config['MONGO_SERVER'], app.config['MONGO_PORT'])
audio_db = mongo_client[app.config['MONGO_DATABASE']]

api = Api(app)
import audio_app.routes.routes