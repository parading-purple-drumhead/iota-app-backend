from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.exceptions import RequestValidationError, ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from routers import post, course, chapter, user, badge, bookmark, notification
from firebase_admin import auth

tags_metadata = [
    {
        "name": "Post",
        "description": "Endpoints related to operations on the **Posts**\
            collection."
    },
    {
        "name": "Course",
        "description": "Endpoints related to operations on the **Courses**\
            collection."
    },
    {
        "name": "User",
        "description": "Endpoints related to operations on the **Users**\
            collection."
    },
    {
        "name": "Badge",
        "description": "Endpoints related to operations on the **Badge**\
            collection."
    },{
        "name": "Notification",
        "description": "Endpoints related to operations on the **Notification**\
            collection."
    }
]

app = FastAPI(
    title="IoTA App Backend",
    description="Backend for the IoT Alliance App",
    version="1.0",
    openapi_tags=tags_metadata
)


@app.middleware("http")
async def verify_token(request: Request, call_next):
    try:
        exclude = ["/docs", "/openapi.json"]

        if request.url.path not in exclude:
            token = request.headers.get("token")
            uid = request.headers.get("uid")
            if auth.verify_id_token(token)["uid"] != uid:
                raise Exception()

        response = await call_next(request)
        return response

    except ValidationError as e:
        print(e)
        return Response(status_code=500, content=str(e))
    except Exception as e:
        print(e)
        return Response(status_code=401, content="Not Authorized!")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(exc)
    return Response(status_code=422, content=str(exc))


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(exc)
    return Response(status_code=exc.status_code, content=exc.detail)

app.include_router(
    post.router,
    prefix="/post",
    tags=["Post"]
)

app.include_router(
    course.router,
    prefix="/course",
    tags=["Course"]
)

app.include_router(
    chapter.router,
    prefix="/chapter",
    tags=["Chapter"]
)

app.include_router(
    user.router,
    prefix="/user",
    tags=["User"]
)

app.include_router(
    badge.router,
    prefix="/badge",
    tags=["Badge"]
)

app.include_router(
    bookmark.router,
    prefix="/bookmark",
    tags=["Bookmark"]
)

app.include_router(
    notification.router,
    prefix="/notification",
    tags=["Notification"]
)