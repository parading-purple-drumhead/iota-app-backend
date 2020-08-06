from fastapi import APIRouter, HTTPException, Request
from models import Chapter
from routers import db


router = APIRouter()


@router.post("/add")
def add_chapter(chapter: Chapter, request: Request):
    try:
        uid = request.headers.get("uid")
        course_id = request.headers.get("course_id")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            collection_ref = db.collection(u"courses").document(course_id).collection(u"chapters")
            collection_ref.add(dict(chapter))

        raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{chapter_id}", response_model=Chapter)
def get_chapter(chapter_id, request: Request):
    try:
        course_id = request.headers.get("course_id")
        course_ref = db.collection(u"courses").document(course_id)
        chapter = course_ref.collection(u"chapters").document(chapter_id).get().to_dict()
        post_ids = chapter["post_ids"]
        chapter["posts"] = []
        for post_id in post_ids:
            post = db.collection(u"posts").document(post_id).get()
            post_dict = post.to_dict()
            post_dict["id"] = post.id
            chapter["posts"].append(post_dict)
        return chapter

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{chapter_id}")
def edit_chapter(chapter_id, chapter: Chapter, request: Request):
    try:
        uid = request.headers.get("uid")
        course_id = request.headers.get("course_id")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            course_ref = db.collection(u"courses").document(course_id)
            chapter_ref = course_ref.collection(u"chapters").document(chapter_id)
            new_data = chapter.dict(exclude_none=True, exclude_defaults=True)
            chapter_ref.update(dict(new_data))

        raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{chapter_id}")
def delete_chapter(chapter_id, request: Request):
    try:
        uid = request.headers.get("uid")
        course_id = request.headers.get("course_id")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            course_ref = db.collection(u"courses").document(course_id)
            course_ref.collection(u"chapters").document(chapter_id).delete()

        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
