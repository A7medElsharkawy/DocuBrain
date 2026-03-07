from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId

class Asset(BaseModel):
    id : Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str=Field(...,min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(ge=0, default=None) #ge is greater than or equal to and default is 0
    asset_cofig: dict = Field(default=None)
    asset_pushed_at: datetime = Field(default=datetime.utcnow)


    class Config: # this class is used to allow the arbitrary types allowed (ObjectId)
        arbitrary_types_allowed = True
    
    @classmethod
    def get_indexes(cls):

        return[
            {
                "key":[
                    ("asset_project_id", 1)
                ],
                "name": "asset_project_id_index_1",
                "unique": False
            },
            {
                "key":[
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],
                "name": "asset_project_id_name_index_1",
                "unique": True
            }
        ]