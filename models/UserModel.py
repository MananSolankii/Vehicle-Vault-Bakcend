from typing import Any, Dict, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, validator


class User(BaseModel):
    name: str
    contact: str
    email: str
    password: str


class UserOut(User):
    id: str = Field(alias="_id")
    role: Optional[Dict[str, Any]] = None

    @validator("id", pre=True, always=True)
    def convert_id_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator("role", pre=True, always=True)
    def convert_role_dict(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v


class UserLogin(BaseModel):
    email: str
    password: str