from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId
class Project(BaseModel):
    _id:Optional[str] = None
    project_id:str = Field(..., min_length=1, max_length=100)

    @validator("project_id")
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value
    

    class Config:
        arbitary_types_allowed = True