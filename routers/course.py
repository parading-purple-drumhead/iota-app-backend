from fastapi import APIRouter
from models import course
from routers import db, tokenverify

router = APIRouter()


@router.post("/add")
def addCourse(course: course):

    try:
        if tokenverify(course.token_sent) != course.uid_sent:
            return {
                "status": False,
                "error": "Not authenticated"
            }

        doc_ref = db.collection(u"courses")
        data = {
            "description": course.description,
            "enrollments": 0,
            "name": course.name,
            "rating": 0,
            "posts": course.posts,
            "recommended_courses": course.recommended_courses
        }

        doc_ref.add(data)

        return {
            "status": True
        }

    except Exception as e:
        return {
            "status": False,
            "error": e
        }


@router.post("/edit")
def editCourse(course: course):

    try:
        if tokenverify(course.token_sent) != course.uid_sent:
            return {
                "status": False,
                "error": "Not authenticated"
            }

        edit = db.collection(u"courses").document(course.course_id)
        edit.update({u"name": course.name})
        edit.update({u"post": course.posts})
        edit.update({u"recommended_courses": course.recommended_courses})
        edit.update({u"rating": course.rating})
        edit.update({u"description": course.description})
        edit.update({u"enrollments": course.enrollments})

        return {
            "status": True
        }

    except Exception as e:
        print(e)
        return {
            "status": False,
            "error": e
        }


@router.delete("/delete")
def deleteCourse(course: course):
    try:
        if tokenverify(course.token_sent) != course.uid_sent:
            return {
                "status": False,
                "error": "Not authenticated"
            }

        db.collection(u"courses").document(course.course_id).delete()

        return {
            "status": True
        }

    except Exception as e:
        print(e)
        return {
            "status": False,
            "error": e
        }
