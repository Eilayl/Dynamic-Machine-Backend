from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    ACTIVE = "active"
    NO_ACTIVE = "no_active"


class Machine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=10)
    email: str = Field(index=True)
    location: str
    number: int
    float_number: float
    enum: Status  # Use Status enum for database column
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class MachineCreate(BaseModel):
    name: str
    email: EmailStr
    location: str
    number: int
    float_number: float
    enum: Literal["active", "no_active"] = Field(title="Status")
    password: str


class MachineUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    number: Optional[int] = None
    float_number: Optional[float] = None
    enum: Optional[Literal["active", "no_active"]] = Field(default=None, title="Status")
    password: Optional[str] = None


class MachineRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    location: str
    number: int
    float_number: float
    enum: Literal["active", "no_active"] = Field(title="Status")
    created_at: datetime
    updated_at: Optional[datetime] = None
