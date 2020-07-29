from fastapi import APIRouter, HTTPException, Request
from models import Chapter
from routers import db
from firebase_admin import firestore


router = APIRouter()


@router.post("/add")
def add_chapter(chapter: Chapter, request: Request):
    try:
        uid = request.headers.get("uid")
        course_id = request.headers.get("course_id")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            doc_ref = db.collection(u"chapters")
            chapter_ref = doc_ref.add(dict(chapter))
            print(chapter_ref[1].id)
            course_ref = db.collection("courses").document(course_id)
            course_ref.update({
                u"chapters": firestore.ArrayUnion([chapter_ref[1].id])
            })

        raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{chapter_id}", response_model=Chapter)
def get_chapter(chapter_id):
    try:
        chapter = db.collection(u"chapters").document(chapter_id).get().to_dict()
        return chapter

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{chapter_id}")
def edit_chapter(chapter_id, chapter: Chapter, request: Request):
    try:
        uid = request.headers.get("uid")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            chapter_ref = db.collection(u"chapters").document(chapter_id)
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
            db.collection(u"chapters").document(chapter_id).delete()
            db.collection(u"courses").document(course_id).update({
                u"chapters": firestore.ArrayRemove([chapter_id])
            })
        else:
            raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
