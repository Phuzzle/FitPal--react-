from flask import Flask
from config import db

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.DevelopmentConfig')
    
    # Firebase is already initialized in config.py, so we don't need to do it here
    # Make db available to all app contexts
    app.db = db
    
    # Register blueprints here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
