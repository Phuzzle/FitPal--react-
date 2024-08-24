import os
from myflaskapp import create_app

if __name__ == '__main__':
    if not os.environ.get('FIREBASE_CREDENTIALS'):
        print("Error: FIREBASE_CREDENTIALS environment variable is not set.")
        print("Please set the FIREBASE_CREDENTIALS environment variable to the path of your Firebase credentials JSON file.")
        exit(1)
    
    app = create_app()
    app.run(debug=True)
