"""contains the application configurations"""
import os

class Config(object):
    DEBUG = True
    Database = os.getenv('DATABASE_URL')
    secret_key = "hhjkshufierfrioenfreh"

class Development(Config):
    DEBUG = True
    
class Testing(Config):
    Database = os.getenv('TEST_DATABASE')


config = {
    "testing": Testing,
    "development": Development
}