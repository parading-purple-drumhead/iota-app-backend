from fastapi import APIRouter, HTTPException, Request
from firebase_admin import firestore
from routers import db

router = APIRouter()


@router.post("/{course_id}")
def notifi_user(course_id, request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid)
        if user.collection(u"bookmarks").document(course_id).get().to_dict():
            bookmark_ref = user.collection(u"bookmarks").document(course_id)
            bookmark_dict = bookmark_ref.get().to_dict()
            if(bookmark_dict["type"] == "courses"):
                course_ref = db.collection(u"courses").document(course_id)
                course_ref.update({
                    u"notifi_users": firestore.ArrayUnion([uid])
                })
            else:
                return Exception()
        else:
            return Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{course_id}")
def remove_notifi_user(course_id, request: Request):
    try:
        uid = request.headers.get("uid")
        course_ref = db.collection(u"courses").document(course_id)
        course_ref.update({
            u"notifi_users": firestore.ArrayRemove([uid])
        })

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
