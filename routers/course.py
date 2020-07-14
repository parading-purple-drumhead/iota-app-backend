from fastapi import APIRouter, HTTPException
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
def add_course(course: Course):
    try:
        courses_ref = db.collection(u"courses")
        courses_ref.add(dict(course))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{course_id}")
def edit_course(course_id, course: Course):
    try:

        doc_ref = db.collection(u"courses").document(course_id)
        doc_ref.update(course.dict(exclude_none=True, exclude_defaults=True))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{course_id}")
def delete_course(course_id):
    try:

        doc_ref = db.collection(u"courses").document(course_id)
        doc_ref.delete()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=e)
