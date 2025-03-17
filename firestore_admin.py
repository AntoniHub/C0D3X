import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("C:\CyberGuardian\serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

"""verify = db.collection('clients').document('IIryAnvyxDuNHxJV4NgL').get()
if verify.exists:
    print(verify.to_dict())"""

"""verify = db.collection('clients').order_by('lastVisit').limit(5).get()
for r in verify:
    print(r.to_dict())"""

"""verify = db.collection('clients').order_by('lastVisit').limit(5).get()
for r in verify:
    print(r.id)"""

verify = db.collection('clients').order_by('lastVisit', direction=firestore.Query.DESCENDING).limit_to_last(5).get()
for r in verify:
    print(r.id)
