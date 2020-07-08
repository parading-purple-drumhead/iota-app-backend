from fastapi import APIRouter
from firebase_admin import firestore
from models import post
from routers import db, tokenverify

router = APIRouter()


@router.post("/add")
def addPost(post: post):
    try:
        if tokenverify(post.token_sent) != post.uid_sent:
            return {
                "status": False,
                "error": "Not authenticated"
            }

        doc_ref = db.collection(u"posts")
        data = {
            u"title": post.title,
            u"type": post.post_type,
            u"created_at": firestore.SERVER_TIMESTAMP,
            u"updated_at": firestore.SERVER_TIMESTAMP,
        }

        if post.post_type == "video":
            data.update({
                u"description": post.description,
                u"url": post.url,
                u"resource_url": post.resource_url,
            })

        elif post.post_type == "article":
            data.update({
                u"content": post.content,
                u"resource_url": post.resource_url,
            })

        elif post.post_type == "quiz":
            data.update({
                u"questions": post.questions,
            })

        doc_ref.add(data)

        return {
            "status": True
        }

    except Exception as e:
        print(e)
        return {
            "status": False,
            "error": e
        }


@router.post("/edit")
def editPost(post: post):
    try:
        if tokenverify(post.token_sent) != post.uid_sent:
            return {
                "status": False,
                "error": "Not authenticated"
            }

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

        return {
            "status": True
        }

    except Exception as e:
        return {
            "status": False,
            "error": e
        }


@router.delete("/delete")
def deletePost(post: post):
    try:
        if tokenverify(post.token_sent) != post.uid_sent:
            return {
                "status": False,
                "error": "Not authenticated"
            }

        db.collection(u"posts").document(post.post_id).delete()

        return {
            "status": True
        }

    except Exception as e:
        print(e)
        return {
            "status": False,
            "error": e
        }
