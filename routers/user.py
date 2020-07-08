from fastapi import APIRouter
from firebase_admin import auth
from routers import models
from routers import db

router = APIRouter()


def tokenverify(safe):
    decoded_token = auth.verify_id_token(safe)
    uid = decoded_token["uid"]
    return uid


@router.post("/getInfo")
def getUserInfo(user: models.user):

    try:
        if tokenverify(user.token_sent) != user.uid_sent:
            return {
                "status": False,
                "error": "Not authenticated"
            }

        doc_ref = db.collection(u"users").document(user.uid_sent)
        user = doc_ref.get()
        if user.exists:
            return {
                "user": user.to_dict(),
                "status": True
            }

    except Exception as e:
        print(e)
        return {
            "status": False,
            "error": e
        }
