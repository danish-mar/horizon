import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'c4d2e2f68f114b2d8d7a2f3a8e9b1c6f7e8d9f3b6a2c5d4e1a8c9b7d6e1f2a3c'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class AlphaTestingConfig(Config):
    SERVER = 'cute.denizuh.com'
    DATABASE = 'nebula'
    DATABASE_CONNECTOR = 'mysql'
    USERNAME = 'root'
    PASSWORD = 'nahida@dendro123'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"{DATABASE_CONNECTOR}://{SERVER}/{DATABASE}"

config = {
    'alphatesting': AlphaTestingConfig,
    'default': AlphaTestingConfig
}