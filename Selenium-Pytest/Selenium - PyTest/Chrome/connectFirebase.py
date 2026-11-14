import os
try:
    from dotenv import load_dotenv
    load_dotenv()  # optional: QA_* variables from an untracked .env file
except ImportError:
    pass
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json"))
firebase_admin.initialize_app(cred)

db = firestore.client()

result = db.collection('clients').document('3hqrdVOkcpXcnYoZjaB9').get()
if result.exists:
    print(result.to_dict())
