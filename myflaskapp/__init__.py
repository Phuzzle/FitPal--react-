from flask import Flask
from firebase_admin import credentials, initialize_app, firestore

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.DevelopmentConfig')
    
    # Initialize Firebase
    cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
    initialize_app(cred)
    db = firestore.client()
    
    # Make db available to all app contexts
    app.db = db
    
    # Register blueprints here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
