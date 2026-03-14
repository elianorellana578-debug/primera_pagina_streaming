
from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    description: str
    genres: str
    year: str
    video_url: str
    is_premium: bool
    
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserOut(BaseModel):
    username: str
    email: str