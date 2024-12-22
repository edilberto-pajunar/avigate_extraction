import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv


# Initialize Firebase with credentials from .env file
def initialize_firestore():
    # Load environment variables from .env file
    load_dotenv("../.env")

    try:
        # Get Firebase JSON configuration from environment variable
        # Parse the config to a dictionary and initialize the app
        cred = credentials.Certificate("serviceKey.json")
        firebase_admin.initialize_app(cred, {
            'projectId': os.getenv('FIREBASE_PROJECT_ID')
        })
        print("Firebase initialized successfully")
    except Exception as e:
        print(e)

    