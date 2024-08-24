import os
from firebase_admin import credentials, initialize_app, firestore, get_app

_firebase_initialized = False

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS') or 'firebase-credentials.json'
    
    @staticmethod
    def init_firebase():
        global _firebase_initialized
        if not _firebase_initialized:
            try:
                # Try to get the existing app
                app = get_app()
            except ValueError:
                # If the app doesn't exist, initialize it
                cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
                app = initialize_app(cred)
            _firebase_initialized = True
        return firestore.client()

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Initialize Firestore client
db = Config.init_firebase()
