from flask import Flask, abort
from firebase_admin import credentials, initialize_app, firestore
import os

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.DevelopmentConfig')
    
    # Initialize Firebase
    firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
    if not firebase_credentials:
        app.logger.error("FIREBASE_CREDENTIALS environment variable is not set.")
        abort(500, description="Server configuration error: Firebase credentials not found.")
    
    try:
        cred = credentials.Certificate(firebase_credentials)
        initialize_app(cred)
        db = firestore.client()
        
        # Make db available to all app contexts
        app.db = db
    except Exception as e:
        app.logger.error(f"Failed to initialize Firebase: {str(e)}")
        abort(500, description="Server configuration error: Failed to initialize Firebase.")
    
    # Register blueprints here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
