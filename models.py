from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Literal
from pydantic import AnyUrl, EmailStr


class Comment(BaseModel):
    id: str
    user_id: str
    content: str


class Post(BaseModel):
    id: Optional[str]
    title: Optional[str]
    type: Optional[Literal["article", "quiz", "video"]]
    created_at: datetime
    updated_at: datetime
    description: Optional[str]
    url: Optional[str]
    resource_url: Optional[AnyUrl]
    content: Optional[str]
    questions: Optional[List[str]] = []
    comments: Optional[List[Comment]]


class Badge(BaseModel):
    image: Optional[str]
    name: Optional[str]
    requirement: Optional[str]


class Chapter(BaseModel):
    id: Optional[str]
    title: Optional[str]
    post_ids: Optional[List[str]] = []
    posts: Optional[List[Post]] = []


class Course(BaseModel):
    description: Optional[str]
    enrollments: Optional[List[str]] = []
    name: Optional[str]
    rating: Optional[float] = 0.0
    chapters: Optional[List[Chapter]] = []
    recommended_courses: Optional[List[str]] = []


class Progress(BaseModel):
    id: Optional[str]
    completion: Optional[datetime]
    course_progress: Optional[float]
    last_accessed: Optional[datetime]
    post_progress: Optional[Dict[str, float]]


class User(BaseModel):
    name: Optional[str]
    avatar: Optional[str]
    admin: Optional[bool]
    email: Optional[EmailStr]
    phone: Optional[str]
    points: Optional[int] = 0
    college: Optional[str]
    joined: datetime
    badge: Optional[List[str]] = []
    progress: Optional[List[Progress]]
    bookmarks: Optional[Dict[str, List[str]]]
    activity: Optional[Dict[str, int]] = None
    recomended_course: Optional[List[str]] = None


class Question(BaseModel):
    question: Optional[str]
    option: Optional[Dict[str, str]]
    answer: Optional[List[str]]
    difficulty: Optional[str]
    number: Optional[int]


class Quiz(BaseModel):
    question: Optional[str]
    option: Optional[Dict[str, str]]
    answer: Optional[List[str]]
    difficulty: Optional[str]
    number: Optional[int]
    response: Optional[str]


class Bookmark(BaseModel):
    type: Optional[Literal["posts", "courses"]]
    id: Optional[str]
