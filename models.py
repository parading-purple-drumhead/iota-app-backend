from pydantic import BaseModel
import datetime


class post(BaseModel):
    title: str
    post_type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: str = None
    url: str = None
    resource_url: str = None
    content: str = None
    questions: list = None


class course(BaseModel):
    description: str
    enrollments: int
    name: str
    rating: float
    posts: list = None
    recommended_courses: list = None


class user(BaseModel):
    name: str
    avatar: str
    email: str
    phone: int
    points: int
