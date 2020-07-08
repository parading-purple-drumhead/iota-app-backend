from fastapi import FastAPI
from routers import post, course, user

app = FastAPI()
app.include_router(
    post.router,
    prefix="/post",
    tags=["post"]
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
