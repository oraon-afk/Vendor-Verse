from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    email: str
    password: str
