from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .database.database import *
from .models.models import *
import urllib.parse
from fastapi import Query
from typing import Optional

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# regex solution: https://www.mongodb.com/community/forums/t/case-insensitive-search-with-regex/120598 
# and if the string is in the variable we can use f strings to escape the qutoes and add the variable to the query.
# To find if the data / value for which the query is fired is in either title field or other names field; {$or: [{title: 'Naruto'}, {other_names: 'Naruto Shippuden'}]}.
@app.get("/", tags=["GET"])
async def root():
    animeData = await get_anime_data(None, None, None, None, None, 1, 15)
    return animeData


@app.get("/anime", tags=["GET"])
async def get_anime_data(
    title: str = Query(None, max_length=50),
    genre: str = Query(None, max_length=50),
    released_date: str = Query(None, max_length=50),
    status: str = Query(None, max_length=50),
    category: str = Query(None, max_length=50),
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=1000)
):
    filters = {}
    
    if title:
        filters["$or"] = [
            {"title": {"$regex": title, "$options": "i"}},
            {"other_names": {"$regex": title, "$options": "i"}}
        ]
    
    if genre:
        filters["genre"] = {"$regex": genre, "$options": "i"}
    
    if released_date:
        filters["released"] = {"$regex": released_date, "$options": "i"}
    
    if status:
        filters["status"] = {"$regex": status, "$options": "i"}
    
    if category:
        filters["anime_type"] = {"$regex": category, "$options": "i"}
    
    total_records = await collection.count_documents(filters)
    skip = (page - 1) * limit
    animeResponse = collection.find(filters).skip(skip).limit(limit)
    
    animeData = []
    async for i in animeResponse:
        animeData.append(AnimeData(**i))
    
    return ResponseModel(
        response_code="HTTPS 200 OK",
        message="Success",
        payload=animeData,
        total=total_records,
        page=page,
        limit=limit
    )