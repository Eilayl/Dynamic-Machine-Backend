from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    ACTIVE = "active"
    NOT_ACTIVE = "not_active"


# זה הטבלה במסד הנתונים
class Machine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=10)
    email: EmailStr
    location: str
    number: int
    float_number: float
    enum: Status
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


# זה schema ל־POST
class MachineCreate(BaseModel):
    name: str
    email: EmailStr
    location: str
    number: int
    float_number: float
    enum: Status
    password: str


# זה schema ל־PUT/PATCH
class MachineUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    number: Optional[int] = None
    float_number: Optional[float] = None
    enum: Optional[Status] = None
    password: Optional[str] = None


# זה schema ל־GET (מה שתחזיר ללקוח)
class MachineRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    location: str
    number: int
    float_number: float
    enum: Status
    created_at: datetime
    updated_at: Optional[datetime] = None
