import firebase_admin
from firebase_admin import auth, credentials, firestore, messaging

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def tokenverify(safe):
    decoded_token = auth.verify_id_token(safe)
    uid = decoded_token["uid"]
    return uid


def send_message_to_topic(notification, data, topic):
    try:
        message = messaging.Message(notification=messaging.Notification(
            title=notification["title"], body=notification["body"]), data=data, topic=topic)
        response = messaging.send(message)
        print(response)

    except Exception as e:
        return (e)
