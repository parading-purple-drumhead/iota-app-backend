from fastapi import APIRouter, HTTPException, Request
from models import User, ReturnUser, Progress
from routers import db
from routers.badge import calculate_badge
from google.api_core.exceptions import AlreadyExists
from firebase_admin import firestore
import datetime
from dateutil.relativedelta import relativedelta
import calendar
from collections import OrderedDict

router = APIRouter()


def count_completed(d):
    keys = 0
    values = 0
    for item in d.keys():
        if isinstance(d[item], (dict)):
            keys += 1
            k, v = count_completed(d[item])
            values += v
            keys += k
        else:
            keys += 1
            values += 1

    return keys, values


def cprogress(user_id):
    try:
        update = db.collection(u"users").document(user_id).collection(u"progress").stream()
        user = db.collection("users").document(user_id)
        courses = []
        j = 0
        quiz = []
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
            f, post_completed = count_completed(edit)
            course_progress = post_completed / post_c
            user.set({u"course_progress": {courses[j]: course_progress}}, merge=True)
            j = j + 1
            try:
                for i in edit["quiz_progress"].keys():
                    quiz.append(i)

            except KeyError as e:
                print(e)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

    return quiz


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


@router.get("/activity")
def activity(request: Request):
    try:
        uid = request.headers.get("uid")
        act = db.collection(u"users").document(uid).get().to_dict()
        act = act["activity"]
        if(act is None):
            total = {}
            total.update({"Daily": None})
            total.update({"Weekly": None})
            total.update({"Monthly": None})

            return total

        daily = {}
        today = datetime.datetime.now()
        for i in range(7):
            sdate = datetime.timedelta(days=i)
            var1 = today-sdate
            date = str(var1.date())
            if(date not in act.keys()):
                daily.update({date: 0})
            else:
                daily.update({date: act[date]})

        # monthly
        listofdates = []
        today = today.date()
        sdate = today - relativedelta(months=+6)
        sdate = sdate.replace(day=1)
        delta = today - sdate

        for i in range(delta.days + 1):
            day = sdate + relativedelta(days=i)
            listofdates.append(day)
        listwithvalues = {}
        monthly = {}
        for i in listofdates:
            j = i
            i = i.strftime("%Y-%m-%d").replace("-0", "-")
            i = str(i)

            try:
                j = str(j)
                listwithvalues[i] = act[j]
            except KeyError:
                listwithvalues[i] = 0

        months = set()
        for a in listwithvalues:
            y, m, d = a.split("-")
            months.add(int(m))

        months = sorted(months)

        values = [0]*7
        for i in listwithvalues:
            j = i
            y, month, d = i.split("-")
            month = int(month)
            if(month in months):
                var1 = values[months.index(int(month))]
                values[months.index(int(month))] = var1 + listwithvalues[j]

        for i in range(7):
            j = int(months[i])
            monthly[calendar.month_name[j]] = values[i]

        weeks = {}
        result = []
        for i in range(49):
            dates = datetime.timedelta(days=i)
            dat = today - dates
            result.append(dat)
        a = 0
        b = 7
        for i in range(7):
            sum = 0
            for j in range(a, b):
                try:
                    var = result[j]
                    var = str(var)
                    var = act[var]
                except KeyError:
                    var = 0
                sum = sum + var
            m = result[j]
            a = a + 7
            b = b + 7
            weeks.update({m: sum})
        weeks = OrderedDict(sorted(weeks.items()))
        daily = OrderedDict(sorted(daily.items()))
        total = {}
        total.update({"Daily": daily})
        total.update({"Weekly": weeks})
        total.update({"Monthly": monthly})
        return total

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=ReturnUser)
def get_user_info(user_id):

    try:
        recommended_course(user_id)
        q = cprogress(user_id)
        user_ref = db.collection(u"users").document(user_id)
        user = user_ref.get().to_dict()

        if user["course_progress"] is None:
            user["course_progress"] = {}

        if user["activity"] is None:
            user["activity"] = {}

        if user["recommended_course"] is None:
            user["recommended_course"] = []

        user["bookmarks"] = []
        bookmarks_ref = user_ref.collection(u"bookmarks").get()
        for bookmark_ref in bookmarks_ref:
            bookmark_dict = bookmark_ref.to_dict()
            if bookmark_dict["type"] == "courses":
                user["bookmarks"].append(bookmark_dict["course_id"])
            else:
                user["bookmarks"].append(bookmark_dict["post_id"])

        if user["updated_at"] is not None:

            c = {}
            c = user["updated_at"]
            s = sorted(c.items(), key=lambda x: x[1], reverse=True)
            v = dict(s).keys()
            li = list(v)

            cp = db.collection("users").document(user_id).get().to_dict()
            var = cp["course_progress"]
            cp_updated = {}
            j = 0
            for i in li:
                cp_updated.update({li[j]: var[li[j]]})
                j = j + 1

            del user["course_progress"]
            user["course_progress"] = cp_updated

        else:
            user["updated_at"] = {}

        user["badge"] = calculate_badge(user_id)

        user["quiz_progress"] = q
        act = user["activity"]
        points = sum(act.values())
        user["points"] = points

        return user

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}")
def edit_user(user_id, user: User, request: Request):
    try:
        uid = request.headers.get("uid")
        if user_id == uid:
            user_ref = db.collection(u"users").document(user_id)
            user_ref.update(user.dict(exclude_none=True, exclude_defaults=True))
        else:
            raise Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{user_id}/add")
def add_user(user_id, user: User):
    try:
        user_ref = db.collection(u"users")
        user_ref.add(dict(user), document_id=user_id)
        a = "MLVPBwIxRQ0yYKSbMAq2"
        b = "eUqXuVM1R47tXSSzj9uQ"
        addreco = db.collection(u"users").document(user_id)
        addreco.update({u"recommended_course": firestore.ArrayUnion([a])})
        addreco.update({u"recommended_course": firestore.ArrayUnion([b])})

    except AlreadyExists as e:
        print(e)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
def delete_user(user_id, request: Request):
    try:
        uid = request.headers.get("uid")
        if user_id == uid:
            db.collection(u"users").document(user_id).delete()
        else:
            raise Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{course_id}/progress")
def progress(request: Request, course_id, progress: Progress):
    try:
        uid = request.headers.get("uid")
        activity = db.collection(u"users").document(uid)
        update = db.collection(u"users").document(uid).collection(u"progress").document(course_id)
        type_of_post = db.collection(u"posts").document(progress.post_id).get().to_dict()
        if(type_of_post["type"] == "quiz"):
            update.set({u"quiz_progress": {progress.post_id: progress.progress}}, merge=True)
        elif(type_of_post["type"] == "video"):
            update.set({u"video_progress": {progress.post_id: progress.progress}}, merge=True)
        elif(type_of_post["type"] == "article"):
            update.set({u"article_progress": {progress.post_id: progress.progress}}, merge=True)
        activity.update({"updated_at": {course_id: firestore.SERVER_TIMESTAMP}})
        today = str(datetime.date.today())
        pointt = int(progress.points)
        activity.update({u"activity": {today: firestore.Increment(pointt)}})
        return {progress.post_id: progress.progress}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
