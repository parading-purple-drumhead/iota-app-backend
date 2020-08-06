from fastapi import APIRouter, HTTPException, Request
from models import Course
from typing import Dict
from routers import db

router = APIRouter()


@router.get("", response_model=Dict[str, Course])
def get_all_courses():
    try:
        courses_ref = db.collection(u"courses")
        courses = courses_ref.get()
        data = {}
        for course in courses:
            course_ref = courses_ref.document(course.id)
            course_doc = course_ref.get().to_dict()
            # chapters = course_ref.collection(u"chapters").get()
            # course_doc["chapters"] = []
            # for chapter in chapters:
            #     chapter_dict = chapter.to_dict()
            #     chapter_dict["id"] = chapter.id
            #     course_doc["chapters"].append(chapter_dict)
            data[course.id] = course_doc
        return data

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{course_id}", response_model=Course)
def get_course(course_id):
    try:
        course_ref = db.collection(u"courses").document(course_id)
        course = course_ref.get().to_dict()
        chapters = course_ref.collection(u"chapters").get()
        course["chapters"] = []
        for chapter in chapters:
            chapter_dict = chapter.to_dict()
            post_ids = chapter_dict["post_ids"]
            chapter_dict["posts"] = []
            for post_id in post_ids:
                post = db.collection(u"posts").document(post_id).get()
                post_details = post.to_dict()
                post_dict = {}
                post_dict["id"] = post.id
                post_dict["title"] = post_details["title"]
                post_dict["type"] = post_details["type"]
                chapter_dict["posts"].append(post_dict)
            chapter_dict["id"] = chapter.id
            course["chapters"].append(chapter_dict)
        return course

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add")
def add_course(course: Course, request: Request):
    try:
        uid = request.headers.get("uid")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            courses_ref = db.collection(u"courses")
            courses_ref.add(dict(course))
        raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{course_id}")
def edit_course(course_id, course: Course, request: Request):
    try:
        uid = request.headers.get("uid")
        doc_ref = db.collection(u"users").document(uid).get().to_dict()
        if doc_ref["admin"]:
            doc = db.collection(u"courses").document(course_id)
            doc.update(course.dict(exclude_none=True, exclude_defaults=True))
        raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{course_id}")
def delete_course(course_id, request: Request):
    try:
        uid = request.headers.get("uid")
        doc = db.collection(u"users").document(uid).get().to_dict()
        if doc["admin"]:
            doc_ref = db.collection(u"courses").document(course_id)
            doc_ref.delete()
        raise Exception()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
