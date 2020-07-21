from fastapi import APIRouter, HTTPException, Request
from models import Course
from typing import Dict
from routers import db

router = APIRouter()


@router.get("", response_model=Dict[str, Course])
def get_all_courses():
    try:
        courses_ref = db.collection(u"courses").stream()
        data = {}
        for course in courses_ref:
            data[course.id] = course.to_dict()
        return data

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{course_id}", response_model=Course)
def get_course(course_id):
    try:
        course = db.collection(u"courses").document(course_id).get().to_dict()
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
