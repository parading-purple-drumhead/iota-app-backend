from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from routers import post, course, user
from firebase_admin import auth

tags_metadata = [
    {
        "name": "Post",
        "description": "Endpoints related to operations on the **Post**\
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
        exclude = ['/docs', '/openapi.json']

        if request.url.path not in exclude:
            token = request.headers.get('token')
            uid = request.headers.get('uid')
            if auth.verify_id_token(token).uid != uid:
                raise Exception()

        response = await call_next(request)
        return response

    except Exception as e:
        print(e)
        return Response(status_code=401, content="Not Authorized!")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return Response(status_code=422, content=str(exc))


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return Response(status_code=exc.status_code, content=exc.detail)

app.include_router(
    post.router,
    prefix="/post",
    tags=["Post"]
)

app.include_router(
    course.router,
    prefix="/course",
    tags=["course"]
)

app.include_router(
    user.router,
    prefix="/user",
    tags=["user"]
)
