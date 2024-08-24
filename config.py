import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS') or 'path/to/your/firebase-credentials.json'
    # Add other configuration variables here

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
