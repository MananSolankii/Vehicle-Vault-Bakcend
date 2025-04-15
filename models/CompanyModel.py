from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class Company(BaseModel):
    name: str

class CompanyOut(Company):
    id: str = Field(alias="_id")  # Convert ObjectId to string

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def convert_Objectid(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if "_id" in data:  # ✅ Fix: Check if '_id' exists
            data["id"] = self.convert_Objectid(data["_id"])
            del data["_id"]  # ✅ Remove '_id' after conversion
        return data
