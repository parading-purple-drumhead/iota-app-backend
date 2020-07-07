import firebase_admin
from firebase_admin import firestore, auth
from firebase_admin import credentials
from fastapi import FastAPI
import models

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()


def tokenverify(safe):
    decoded_token = auth.verify_id_token(safe)
    uid = decoded_token["uid"]
    return uid


@app.post("/addPost")
def addPost(post: models.post):
    try:
        if tokenverify(post.token_sent) != post.uid_sent:
            return {"status": False, "error": "Not authenticated"}

        doc_ref = db.collection(u"posts")
        data = {
            u"title": post.title,
            u"type": post.post_type,
            u"created_at": firestore.SERVER_TIMESTAMP,
            u"updated_at": firestore.SERVER_TIMESTAMP,
        }

        if post.post_type == "video":
            data.update(
                {
                    u"description": post.description,
                    u"url": post.url,
                    u"resource_url": post.resource_url,
                }
            )

        elif post.post_type == "article":
            data.update(
                {u"content": post.content, u"resource_url": post.resource_url}
            )

        elif post.post_type == "quiz":
            data.update(
                {u"questions": post.questions}
            )

        doc_ref.add(data)

        return {"status": True}

    except Exception as e:
        print(e)
        return {"status": False, "error": e}


@app.post("/editPost")
def editPost(post: models.post):
    try:
        if tokenverify(post.token_sent) != post.uid_sent:
            return {"status": False, "error": "Not authenticated"}

        edit = db.collection(u"posts").document(post.post_id)
        edit.update({u"title": post.title})
        edit.update({u"updated_at": firestore.SERVER_TIMESTAMP})

        if post.post_type == "video":

            edit.update({u"description": post.description})
            edit.update({u"resource_url": post.resource_url})
            edit.update({u"url": post.url})

        elif post.post_type == "article":

            edit.update({u"content": post.content})
            edit.update({u"resource_url": post.resource_url})

        else:
            edit.update({u"questions": post.questions})

        return {"status": True}

    except Exception as e:
        return {"status": False, "error": e}


@app.delete("/deletePost")
def deletePost(post: models.post):
    try:
        if tokenverify(post.token_sent) != post.uid_sent:
            return {"status": False, "error": "Not authenticated"}

        db.collection(u"posts").document(post.post_id).delete()

        return {"status": True}

    except Exception as e:
        print(e)
        return {"status": False, "error": e}


@app.post("/addCourse")
def addCourse(course: models.course):

    try:
        if tokenverify(course.token_sent) != course.uid_sent:
            return {"status": False, "error": "Not authenticated"}

        doc_ref = db.collection(u"courses")
        data = {
            "description": course.description,
            "enrollments": 0,
            "name": course.name,
            "rating": 0,
            "posts": course.posts,
            "recommended_courses": course.recommended_courses,
        }

        doc_ref.add(data)

        return {"status": True}

    except Exception as e:
        return {"status": False, "error": e}


@app.delete("/deleteCourse")
def deleteCourse(course: models.course):
    try:
        if tokenverify(course.token_sent) != course.uid_sent:
            return {"status": False, "error": "Not authenticated"}

        db.collection(u"courses").document(course.course_id).delete()

        return {"status": True}

    except Exception as e:
        print(e)
        return {"status": False, "error": e}


@app.post("/editCourse")
def course(course: models.course):

    try:
        if tokenverify(course.token_sent) != course.uid_sent:
            return {"status": False, "error": "Not authenticated"}

        edit = db.collection(u"courses").document(course.course_id)
        edit.update({u"name": course.name})
        edit.update({u"post": course.posts})
        edit.update({u"recommended_courses": course.recommended_courses})
        edit.update({u"rating": course.rating})
        edit.update({u"description": course.description})
        edit.update({u"enrollments": course.enrollments})

        return {"status": True}

    except Exception as e:
        print(e)
        return {"status": False, "error": e}


@app.post("/userInfo")
def getUserInfo(user: models.user):

    try:
        if tokenverify(user.token_sent) != user.uid_sent:
            return {"status": False, "error": "Not authenticated"}

        doc_ref = db.collection(u"users").document(user.uid_sent)
        user = doc_ref.get()
        if user.exists:
            return {"user": user.to_dict(), "status": True}

    except Exception as e:
        print(e)
        return {"status": False, "error": e}
