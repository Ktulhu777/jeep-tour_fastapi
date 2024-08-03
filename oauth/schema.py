from datetime import datetime
from typing import Optional
from typing_extensions import Self
from re import fullmatch

from pydantic import BaseModel, model_validator, Field, field_validator, EmailStr
from fastapi import HTTPException, status

from .validators import password_validate


class RegisterUser(BaseModel):
    username: str = Field(min_length=4)
    phone: str
    password_1: str
    password_2: str

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, phone: str) -> str:
        if not fullmatch(r'(\+7|8)\D*\d{3}\D*\d{3}\D*\d{2}\D*\d{2}', phone):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect phone number")
        return phone

    @model_validator(mode='after')
    def check_passwords(self) -> Self:
        pw1 = self.password_1
        pw2 = self.password_2
        if pw1 != pw2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Passwords are not equal!")
        if password_validate(password=pw1):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="The password must contain Latin letters and numbers")
        return self


class ChangePassword(BaseModel):
    old_password: str
    password_1: str
    password_2: str

    @model_validator(mode='after')
    def check_passwords(self) -> Self:
        pw1 = self.password_1
        pw2 = self.password_2
        if pw1 != pw2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Passwords are not equal!")
        if password_validate(password=pw1):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="The password must contain Latin letters and numbers")
        return self


class GetUser(BaseModel):
    id: int
    username: str
    phone: str
    email: Optional[EmailStr] = None


class GetMeUser(GetUser):
    url: str
    register_data: datetime
    is_active: bool
    is_superuser: bool
    is_verified: bool
