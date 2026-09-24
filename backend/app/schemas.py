from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CaptchaOut(BaseModel):
    token: str
    question: str


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = ""
    captcha_token: str
    captcha_answer: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str
    captcha_token: str
    captcha_answer: str


class AdminLoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str
    model_config = ConfigDict(from_attributes=True)


class AuthOut(BaseModel):
    user: UserOut


class ProductOut(BaseModel):
    id: str
    cat_key: str
    price: float
    img: str
    active: bool
    model_config = ConfigDict(from_attributes=True)


class ProductUpdateIn(BaseModel):
    price: Optional[float] = None
    img: Optional[str] = None
    active: Optional[bool] = None
    cat_key: Optional[str] = None


class OrderItemOut(BaseModel):
    product_id: str
    product_name: str
    qty: int
    unit_price: float
    model_config = ConfigDict(from_attributes=True)


class OrderOut(BaseModel):
    id: int
    status: str
    lang: str
    total: float
    project_nome: str
    project_email: str
    project_desc: str
    custom_sizes: dict
    art_path: str
    art_name: str
    created_at: datetime
    items: list[OrderItemOut]
    model_config = ConfigDict(from_attributes=True)


class OrderStatusIn(BaseModel):
    status: str


class OAuthAvailability(BaseModel):
    google: bool
    facebook: bool
