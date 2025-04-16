from pydantic import BaseModel, EmailStr, validator, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str ="viewer"

    @validator('role')
    def validate_role(cls, v):
        if v not in ['admin', 'developer', 'viewer']:
            raise ValueError('Role must be admin, developer, or viewer')
        return v
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    role: Optional[str] = None
    
    @validator('role')
    def validate_role(cls, v):
        if v and v not in ['admin', 'developer', 'viewer']:
            raise ValueError('Role must be admin, developer, or viewer')
        return v
    
class UserInDB(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class UserResponse(UserBase):
    id: int
    role: str

    model_config = ConfigDict(
        from_attributes=True
    )

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
