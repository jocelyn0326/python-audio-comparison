from datetime import datetime
from typing import Optional

from bson import Binary, ObjectId
from pydantic import BaseModel


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v == "":
            raise TypeError("ObjectId is empty")
        if ObjectId.is_valid(v) is False:
            raise TypeError("ObjectId invalid")
        return str(v)


class MongoBaseModel(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            """Camel case generator"""
            temp = string.split("_")
            return temp[0] + "".join(ele.title() for ele in temp[1:])


class CiModel(MongoBaseModel):
    id: Optional[OID]
    channel: str
    timestamp: int
    ci_value: Optional[Binary] = None
    created_at: datetime = None
    updated_at: datetime = None
