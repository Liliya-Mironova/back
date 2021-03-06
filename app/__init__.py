from flask import Flask, jsonify, url_for
from flask_jsonrpc import JSONRPC
from instance import config
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, VK

import base64
import boto3

# centrifugo
from cent import Client
from flask_cors import CORS

# caching (Memcache)
from werkzeug.contrib.cache import MemcachedCache

# profiler middleware
from werkzeug.contrib.profiler import ProfilerMiddleware

# ORM
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# celery
from .flask_celery import make_celery

# mail
from flask_mail import Mail

# Elasticsearch
from elasticsearch import Elasticsearch


app = Flask(__name__, instance_relative_config=True)
# jsonrpc = JSONRPC(app, '/api/')

CORS(app)
jsonrpc = JSONRPC(app, '/')

# config
app.config.from_pyfile('config.py') # default config
app.config.from_pyfile('config.py', silent=True) # local config

# centrifugo (messages)
cent_client = Client(config.CENTRIFUGO_URL, api_key=config.CENTRIFUGO_API_KEY, timeout=1)

# memcache
# sudo service memcached restart
cache = MemcachedCache([config.MEMCACHE_URL])

# profiler middleware
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

# boto3 (files)
s3_session = boto3.session.Session()
s3_client = s3_session.client(
    service_name='s3',
    endpoint_url=config.S3_ENDPOINT_URL,
    aws_access_key_id=config.S3_ACCESS_KEY_ID,
    aws_secret_access_key=config.S3_SECRET_ACCESS_KEY)

# authentication
oauth = OAuth(app)

# ORM
db = SQLAlchemy(app)

# celery
celery = make_celery(app)

# Elasticsearch
es = Elasticsearch(config.ELASTICSEARCH_URL)

# mail
mail =  Mail(app)


from .views import *
from .models import *