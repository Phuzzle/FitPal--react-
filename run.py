import os
from dotenv import load_dotenv
from myflaskapp import create_app

# Load environment variables from .env file
print("Attempting to load .env file...")
load_dotenv(verbose=True)

# Debug: Print .env file contents (safely)
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as env_file:
        print("Contents of .env file:")
        for line in env_file:
            if line.strip() and not line.startswith('#'):
                key = line.split('=')[0]
                print(f"{key}=[HIDDEN]")
else:
    print(".env file not found!")

if __name__ == '__main__':
    if not os.environ.get('FIREBASE_CREDENTIALS'):
        print("Error: FIREBASE_CREDENTIALS environment variable is not set.")
        print("Please check your .env file and ensure FIREBASE_CREDENTIALS is set to the path of your Firebase credentials JSON file.")
        exit(1)
    
    app = create_app()
    app.run(debug=True)
