import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get("SECRET_KEY")

class Development(Config):
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV  ='Development'
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
class Testing(Config):
    pass

class Staging(Config):
    pass

class Production(Config):
    pass