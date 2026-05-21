"""
Pydantic schemas for authentication
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class SignUpSchema(BaseModel):
    """Schema for user registration"""
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8)
    role: str = Field(..., pattern=r'^(customer|provider|admin)$')


class LoginSchema(BaseModel):
    """Schema for user login"""
    phone_number: str
    password: str


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    full_name: str


class UserResponse(BaseModel):
    """Schema for user data response"""
    id: str
    full_name: str
    phone_number: str
    email: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
