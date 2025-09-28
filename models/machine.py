from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel
from sqlmodel import Field
from typing import Optional
from enum import Enum
class Status(str, Enum):
    ACTIVE = "active"
    NO_ACTIVE = "no_active"

class Machine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(max_length=10)
    location: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    number: Optional[int] = Field(default=None)
    float_number: Optional[float] = Field(default=None)
    enum: Optional[Status] = Field(default=None)
    password: Optional[str] = Field(default=None)
