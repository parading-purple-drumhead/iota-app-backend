from fastapi import APIRouter, HTTPException, Request
from models import User, ReturnUser, Progress
from routers import db
from google.api_core.exceptions import AlreadyExists
from firebase_admin import firestore
from datetime import date

router = APIRouter()


def cprogress(user_id):
    try:
        update = db.collection(u"users").document(user_id).collection(u"progress").stream()
        user = db.collection("users").document(user_id)

        courses = []
        j = 0
        for cprogress in update:
            courses.append(cprogress.id)
            count = db.collection(u"courses").document(courses[j]).collection("chapters").stream()
            chapters = []
            post_c = 0
            for chap in count:
                chapters.append(chap.id)

            c = db.collection(u"courses").document(courses[j]).collection("chapters")
            i = 0
            for i in range(len(chapters)):
                counts = c.document(chapters[i]).get().to_dict()
                k = len(counts["post_ids"])
                post_c = post_c + k
                i = i + 1

            up = db.collection(u"users").document(user_id)
            update = up.collection(u"progress").document(courses[j])
            edit = update.get().to_dict()
            post_count = len(edit["post_progress"])
            post_completed = 0
            k = 0
            for k in range(post_count):
                if list(edit["post_progress"].values())[k] == "1":
                    post_completed = post_completed + 1

                k = k + 1

            course_progress = post_completed/post_c
            user.set({u"course_progress": {courses[j]: course_progress}}, merge=True)
            j = j + 1

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


def recommended_course(user_id):
    try:
        courses = db.collection(u"users").document(user_id).collection(u"progress").stream()
        course = []
        for reco in courses:
            course.append(reco.id)

        i = 0
        j = 0
        recommended_course = set()
        for i in range(len(course)):
            q = db.collection("courses").document(course[i]).get().to_dict()
            for j in range(len(q["recommended_courses"])):
                recommended_course.add(q["recommended_courses"][j])
                j = j + 1

            i = i + 1

        recommended_courses = list(recommended_course)
        k = 0
        for k in range(len(recommended_courses)):
            edit = db.collection(u"users").document(user_id)
            edit.update({
                u"recommended_course": firestore.ArrayUnion([recommended_courses[k]])
            })
            k = k + 1

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=ReturnUser)
def get_user_info(user_id):

    try:
        recommended_course(user_id)
        cprogress(user_id)
        user = db.collection(u"users").document(user_id).get().to_dict()

        if user["course_progress"] is None:
            user["course_progress"] = {}

        if user["activity"] is None:
            user["activity"] = {}

        if user["bookmarks"] is None:
            user["bookmarks"] = {}
        else:
            bookmarks_list = user["bookmarks"]
            user["bookmarks"] = []
            for post_bookmark in bookmarks_list["posts"]:
                user["bookmarks"].append(post_bookmark)
            for course_bookmark in bookmarks_list["courses"]:
                user["bookmarks"].append(course_bookmark)

        if user["recommended_course"] is None:
            user["recommended_course"] = []

        return user

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}")
def edit_user(user_id, user: User):
    try:
        user_ref = db.collection(u"users").document(user_id)
        user_ref.update(user.dict(exclude_none=True, exclude_defaults=True))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{user_id}/add")
def add_user(user_id, user: User):
    try:
        user_ref = db.collection(u"users")
        user_ref.add(dict(user), document_id=user_id)

    except AlreadyExists as e:
        print(e)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
def delete_user(user_id):
    try:
        db.collection(u"users").document(user_id).delete()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{course_id}/progress")
def progress(request: Request, course_id, progress: Progress):
    try:
        uid = request.headers.get("uid")
        activity = db.collection(u"users").document(uid)
        update = db.collection(u"users").document(uid).collection(u"progress").document(course_id)
        update.set({u"post_progress": {progress.post_id: progress.progress}}, merge=True)
        today = str(date.today())
        pointt = int(progress.points)
        activity.update({u"activity": {today: firestore.Increment(pointt)}})

        return {progress.post_id: progress.progress}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
