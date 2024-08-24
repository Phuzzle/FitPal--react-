from flask import Flask
from config import db

from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from .main.views import main
from .auth import auth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Firebase
    Config.init_firebase()

    # Initialize JWT
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
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
