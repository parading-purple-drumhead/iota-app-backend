from fastapi import APIRouter, HTTPException, Request
from models import Bookmark
from routers import db
from firebase_admin import firestore


router = APIRouter()


@router.post("")
def add_bookmark(bookmark: Bookmark, request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid)
        user.update({
            "bookmarks."+bookmark.type: firestore.ArrayUnion([bookmark.id])
        })

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("")
def remove_bookmark(bookmark: Bookmark, request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid)
        user.update({
            "bookmarks."+bookmark.type: firestore.ArrayRemove([bookmark.id])
        })

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
