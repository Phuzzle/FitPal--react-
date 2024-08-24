from . import main

@main.route('/')
def index():
    return "Hello, World!"

# Add more route handlers here
