import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Firebase JSON configuration from environment variable
firebase_config = os.getenv("FIREBASE_CONFIG")

if (firebase_config):
    service_account_info = json.loads(firebase_config)

    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)

    # Initialize Firestore
    db = firestore.client()

    # Fetch a Single Document
    doc_ref = db.collection("Tenant").document("gmiYIQxWyafY91gD8us9")
    doc = doc_ref.get()

    if (doc.exists):
        print(f"Document data: ${doc.to_dict()}")
    else:
        print("No such document!")

    # Fetch All Multiple Documents in a Collection
    # docs = db.collection("Tenant").stream()
    # for doc in docs:
    #     print(f"{doc.id}: {doc.to_dict()}")
else:
    print("FIREBASE_CONFIG not found in .env")


