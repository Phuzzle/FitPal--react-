from flask import Blueprint

main = Blueprint('main', __name__)

from . import views

# The views will be imported when the blueprint is registered in __init__.py
