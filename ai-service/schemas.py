from pydantic import BaseModel, EmailStr
from pydantic import Field
from typing import Optional
password: str = Field(min_length=6)

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChatRequest(BaseModel):
    user_id: int
    question: str
    conversation_id: Optional[int] = None



class ChatResponse(BaseModel):
    answer: str