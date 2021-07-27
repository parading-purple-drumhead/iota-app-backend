from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Literal
from pydantic import AnyUrl, EmailStr


class Comment(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    user_name: Optional[str]
    user_avatar: Optional[str]
    content: Optional[str]
    created_at: Optional[datetime]


class Question(BaseModel):
    question: Optional[str]
    option: Optional[Dict[str, str]]
    answer: Optional[List[str]]
    difficulty: Optional[str]
    number: Optional[int]


class Post(BaseModel):
    id: Optional[str]
    title: Optional[str]
    type: Optional[Literal["article", "quiz", "video"]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    description: Optional[str]
    url: Optional[str]
    resource_url: Optional[Dict[str, AnyUrl]]
    content: Optional[str]
    questions: Optional[Dict[str, Question]] = []
    progress: Optional[float]
    length: Optional[int]


class Badge(BaseModel):
    image: Optional[str]
    name: Optional[str]
    requirement: Optional[int]


class Chapter(BaseModel):
    id: Optional[str]
    title: Optional[str]
    post_ids: Optional[List[str]] = []
    posts: Optional[List[Post]] = []
    order_no: Optional[int]


class Course(BaseModel):
    description: Optional[str]
    name: Optional[str]
    image: Optional[AnyUrl]
    image2: Optional[AnyUrl]
    rating: Optional[float] = 0.0
    chapters: Optional[List[Chapter]] = []
    recommended_courses: Optional[List[str]] = []
    notify_users: Optional[List[str]] = []
    notify: Optional[bool]


class Progress(BaseModel):
    progress: Optional[str]
    post_id: Optional[str]
    points: Optional[str]


class User(BaseModel):
    name: Optional[str]
    avatar: Optional[str]
    admin: Optional[bool]
    email: Optional[EmailStr]
    phone: Optional[str]
    points: Optional[int] = 0
    college: Optional[str]
    joined: Optional[datetime]
    badge: Optional[Badge]
    activity: Optional[Dict[str, int]] = None
    recommended_course: Optional[List[str]] = None
    course_progress: Optional[Dict[str, float]] = None
    updated_at: Optional[Dict[str, datetime]] = None


class ReturnUser(BaseModel):
    name: Optional[str]
    avatar: Optional[str]
    admin: Optional[bool]
    email: Optional[EmailStr]
    phone: Optional[str]
    points: Optional[int] = 0
    college: Optional[str]
    joined: Optional[datetime]
    badge: Optional[Badge]
    bookmarks: Optional[List[str]]
    activity: Optional[Dict[str, int]] = None
    recommended_course: Optional[List[str]] = None
    course_progress: Optional[Dict[str, float]] = None
    quiz_progress: Optional[List[str]] = None


class Quiz(BaseModel):
    question_id: Optional[str]
    answer: Optional[str]


class Bookmark(BaseModel):
    type: Optional[Literal["posts", "courses"]]
    post_id: Optional[str]
    course_id: Optional[str]
