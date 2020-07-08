from fastapi import APIRouter
from models import user
from routers import db, tokenverify

router = APIRouter()


@router.post("/getInfo")
def getUserInfo(user: user):

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
