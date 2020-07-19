import firebase_admin
from firebase_admin import auth, credentials, firestore, messaging

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def tokenverify(safe):
    decoded_token = auth.verify_id_token(safe)
    uid = decoded_token["uid"]
    return uid
