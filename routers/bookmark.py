from fastapi import APIRouter, HTTPException, Request
from firebase_admin import firestore
from models import Bookmark
from routers import db


router = APIRouter()


@router.post("")
def add_bookmark(bookmark: Bookmark, request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid)
        bookmarks_ref = user.collection(u"bookmarks")
        if(bookmark.type == "courses"):
            course_ref = db.collection(u"courses").document(bookmark.course_id)
            course_ref.update({
                u"bookmarked_users": firestore.ArrayUnion([uid])
            })
        bookmarks_ref.add(dict(bookmark))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def get_bookmarks(request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid)
        bookmarks_ref = user.collection(u"bookmarks").get()
        bookmarks = []
        for bookmark_ref in bookmarks_ref:
            bookmark_dict = bookmark_ref.to_dict()
            bookmark = {}
            if bookmark_dict["type"] == "posts":
                post_ref = db.collection(u"posts").document(bookmark_dict["post_id"]).get()
                post = post_ref.to_dict()
                bookmark["id"] = bookmark_ref.id
                bookmark["course_id"] = bookmark_dict["course_id"]
                bookmark["post_id"] = post_ref.id
                bookmark["title"] = post["title"]
                bookmark["type"] = post["type"]
                bookmarks.append(bookmark)
            else:
                course_ref = db.collection(u"courses").document(bookmark_dict["course_id"]).get()
                course = course_ref.to_dict()
                bookmark["id"] = bookmark_ref.id
                bookmark["course_id"] = bookmark_dict["course_id"]
                bookmark["title"] = course["name"]
                bookmark["type"] = "course"
                bookmarks.append(bookmark)

        return bookmarks

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{bookmark_id}")
def remove_bookmark(request: Request, bookmark_id):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid)
        bookmark_ref = user.collection(u"bookmarks").document(bookmark_id)
        bookmark_dict = bookmark_ref.get().to_dict()
        if(bookmark_dict["type"] == "courses"):
            course_ref = db.collection(u"courses").document(bookmark_dict["course_id"])
            course_ref.update({
                u"bookmarked_users": firestore.ArrayRemove([uid])
            })
        bookmark_ref.delete()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
