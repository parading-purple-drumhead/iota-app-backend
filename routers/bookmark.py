from fastapi import APIRouter, HTTPException, Request
from models import Bookmark
from routers import db
from firebase_admin import firestore


router = APIRouter()


@router.post("/add")
def add_bookmark(bookmark: Bookmark, request: Request):
    try:
        uid = request.headers.get("uid")
        bookmark_ref = db.collection(u"bookmarks").add(dict(bookmark))
        user = db.collection(u"users").document(uid)
        user.update({
            u"bookmarks": firestore.ArrayUnion([bookmark_ref[1].id])
        })

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}")
def remove_bookmark(id, request: Request):
    try:
        uid = request.headers.get("uid")
        db.collection(u"bookmarks").document(id).delete()
        user = db.collection(u"users").document(uid)
        user.update({
            u"bookmarks": firestore.ArrayRemove([id])
        })

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
