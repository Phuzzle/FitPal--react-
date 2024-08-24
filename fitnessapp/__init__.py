from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config, db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Firebase
    db = Config.init_firebase()

    # Initialize JWT
    JWTManager(app)

    # Make db available to all app contexts
    app.db = db

    # Register blueprints
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
