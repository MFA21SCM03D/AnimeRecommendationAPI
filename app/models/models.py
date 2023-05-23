from pydantic import BaseModel, conlist, constr, validator
from typing import Optional, List

""" 
To convert the objectID set by mongodb to str and resolve the objectID and FastAPI Issue.
ObjectID cannot be return as dict or json in fastAPI due to this the following snippet is implemented.
References: https://github.com/tiangolo/fastapi/issues/1515#issuecomment-782835977
            https://stackoverflow.com/questions/63881516/objectid-object-is-not-iterable-error-while-fetching-data-from-mongodb-atlas

# from bson.objectid import ObjectId
# pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

Above method is only used if motor is not used and anything else like pymongo is used to interact with the mongodb server.
Motor resolves the objectID issue internally and does not throw an error.
"""
class AnimeData(BaseModel):
    title: Optional [str]
    anime_type: Optional [str]
    plot_summary: Optional [str]
    genre: List[str]
    released: Optional [str]
    status: Optional [str]
    other_names: Optional [str]
    image: Optional [str]

    
class ResponseModel(BaseModel):
    response_code: str
    message: str
    payload: list
    total: int
    page: int
    limit: int


# @validator('genre', pre=True, whole = True)
# def allow_none(cls, v):
#     return v or None
