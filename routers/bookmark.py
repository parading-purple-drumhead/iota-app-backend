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


@router.get("")
def get_bookmarks(request: Request):
    try:
        uid = request.headers.get("uid")
        user = db.collection(u"users").document(uid).get().to_dict()
        bookmarks_list = user["bookmarks"]
        bookmarks = []
        for post_bookmark_id in bookmarks_list["posts"]:
            post = db.collection(u"posts").document(post_bookmark_id).get()
            post_dict = post.to_dict()
            post_bookmark = {}
            post_bookmark["id"] = post.id
            post_bookmark["title"] = post_dict["title"]
            post_bookmark["type"] = "post"
            post_bookmark["post_type"] = post_dict["type"]
            bookmarks.append(post_bookmark)
        for course_bookmark_id in bookmarks_list["courses"]:
            course = db.collection(u"courses").document(course_bookmark_id).get()
            course_dict = course.to_dict()
            course_bookmark = {}
            course_bookmark["id"] = course.id
            course_bookmark["title"] = course_dict["name"]
            course_bookmark["type"] = "course"
            bookmarks.append(course_bookmark)

        return bookmarks

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{bookmark_id}")
def remove_bookmark(request: Request, bookmark_id):
    try:
        uid = request.headers.get("uid")
        type = request.headers.get("type")
        user = db.collection(u"users").document(uid)
        user.update({
            "bookmarks." + type: firestore.ArrayRemove([bookmark_id])
        })

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
