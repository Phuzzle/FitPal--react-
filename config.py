import os
from firebase_admin import credentials, initialize_app, firestore, get_app

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS') or 'path/to/your/firebase-credentials.json'
    
    @staticmethod
    def init_firebase():
        try:
            # Try to get the existing app
            app = get_app()
        except ValueError:
            # If the app doesn't exist, initialize it
            cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
            app = initialize_app(cred)
        return firestore.client(app)

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
