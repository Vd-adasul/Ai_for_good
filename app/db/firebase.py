import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
# Resolve paths relative to this file (app/db/firebase.py)
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
_CRED_PATH = os.path.join(_PROJECT_ROOT, "serviceAccountKey.json")

cred = None
if os.path.exists(_CRED_PATH):
    cred = credentials.Certificate(_CRED_PATH)
else:
    # prompt user or log warning
    print("Warning: serviceAccountKey.json not found. Firebase features will not work.")

if cred:
    try:
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully.")
    except ValueError:
        # App already initialized
        db = firestore.client()
else:
    db = None

def get_db():
    return db
