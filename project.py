'''
Created on Nov 4, 2017

@author: theSoloBrewer
'''
import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
basedir = os.path.abspath(os.path.dirname(__file__))

#basedir = '/home/anarchos/eclipse-workspace/xl-test/'

APP_NAME = 'FTserver'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, APP_NAME + '.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#SQLALCHEMY_TRACK_MODIFICATIONS = False


FTserver = Flask(__name__, static_url_path="", static_folder="static")
FTserver.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, APP_NAME + '.db')
FTserver.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')
FTserver.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
FTserver.secret_key = '5f4dcc3b5aa765d61d8327deb882cf99'
MA = Marshmallow(FTserver)

db = SQLAlchemy(FTserver, session_options={"autoflush": False})



