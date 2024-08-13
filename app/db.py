import redis
from flask import current_app
# # app/db.py
# from flask import current_app, g
#
# def get_db():
#     if 'db' not in g or g.db.is_connected():
#         g.db = mysql.connector.connect(
#             host=current_app.config['DB_HOST'],
#             port=current_app.config['DB_PORT'],
#             user=current_app.config['DB_USER'],
#             password=current_app.config['DB_PASSWORD'],
#             database=current_app.config['DB_DATABASE'],
#             ssl_verify_identity=False,
#         )
#     return g.db

import mysql.connector
from flask import current_app, g

def get_db():

    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['SERVER'],
            database=current_app.config['DATABASE'],
            user=current_app.config['USERNAME'],
            password=current_app.config['PASSWORD']
        )
    return g.db

def close_db(e=None):

    db = g.pop('db', None)

    if db is not None:
        db.close()

def get_redis():
    if 'redis' not in g:
        g.redis = redis.Redis(
            host=current_app.config['REDIS_HOST'],
            password=current_app.config['REDIS_PASSWORD'],
            port=current_app.config['REDIS_PORT'],
            db=current_app.config['REDIS_DB']
        )
    return g.redis

def close_redis(e=None):
    redis_client = g.pop('redis', None)
    if redis_client is not None:
        redis_client.close()