import os
from dotenv import load_dotenv
from fitnessapp import create_app

# Load environment variables from .env file
load_dotenv()

if __name__ == '__main__':
    if not os.environ.get('FIREBASE_CREDENTIALS'):
        print("Error: FIREBASE_CREDENTIALS environment variable is not set.")
        print("Please check your .env file and ensure FIREBASE_CREDENTIALS is set to the path of your Firebase credentials JSON file.")
        exit(1)
    
    app = create_app()
    app.run(debug=True, use_reloader=True)
