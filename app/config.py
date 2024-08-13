import os
import redis

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'c4d2e2f68f114b2d8d7a2f3a8e9b1c6f7e8d9f3b6a2c5d4e1a8c9b7d6e1f2a3c'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class AlphaTestingConfig(Config):
    SERVER = '127.0.0.1'
    DATABASE = 'nebula'
    DATABASE_CONNECTOR = 'mysql'
    USERNAME = 'root'
    PASSWORD = 'nahida@dendro123'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"{DATABASE_CONNECTOR}://{SERVER}/{DATABASE}"
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'nya@123'
    REDIS_DB = 0


class RedisConfig:
    REDIS_HOST = AlphaTestingConfig.REDIS_HOST
    REDIS_PORT = AlphaTestingConfig.REDIS_PORT
    REDIS_PASSWORD = AlphaTestingConfig.REDIS_PASSWORD
    REDIS_DB = AlphaTestingConfig.REDIS_DB


config = {
    'alphatesting': AlphaTestingConfig,
    'default': AlphaTestingConfig
}