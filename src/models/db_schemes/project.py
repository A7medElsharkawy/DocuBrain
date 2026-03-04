from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class Project(BaseModel):
    id:Optional[ObjectId] = Field(None, alias="_id")
    project_id:str = Field(..., min_length=1, max_length=100)

    @validator("project_id")
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value
    

    class Config:
        arbitrary_types_allowed = True
    

    @classmethod
    def get_indexes(cls): # this function is used to get the indexes for the project collection (index form)
        return [{            
            "key":[
                ("project_id", 1) # 1 mean ascending order and -1 mean descending order
            ],
            "name":"project_id_index_1",
            "unique": True 
            }

        ]

