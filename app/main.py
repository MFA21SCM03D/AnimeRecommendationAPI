from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .database.database import *
from .models.models import *
import urllib.parse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/",tags = ["GET"])
async def root():
    return {"message": "Hello Anime World. This is API for Anime."}

@app.get("/anime/{anime_title}", tags = ["GET"])
async def anime(anime_title: str):
    # regex solution: https://www.mongodb.com/community/forums/t/case-insensitive-search-with-regex/120598 
    # and if the string is in the variable we can use f strings to escape the qutoes and add the variable to the query.
    # To find if the data / value for which the query is fired is in either title field or other names field; {$or: [{title: 'Naruto'}, {other_names: 'Naruto Shippuden'}]}.

    animeTitle = []
    animeResponse = collection.find({'$or': [{'title': {'$regex': anime_title, '$options': 'i'}}, {'other_names': {'$regex': anime_title, '$options': 'i'}}]})
    async for i in animeResponse:
        animeTitle.append(AnimeData(**i))
    return ResponseModel(response_code = status.HTTP_200_OK, message = "Success", payload = animeTitle)

@app.get("/anime/", tags = ["GET"])
async def anime():
    animeData = []
    animeResponse =  collection.find()
    async for i in animeResponse:
        animeData.append(AnimeData(**i))
    return ResponseModel(response_code = status.HTTP_200_OK, message = "Success", payload = animeData)

@app.get("/anime/genre/{anime_genre}", tags = ["GET"])
async def anime(anime_genre: str):
    animeGenre = []
    animeResponse = collection.find({'genre': {'$regex': anime_genre, '$options': 'i'}})
    async for i in animeResponse:
        animeGenre.append(AnimeData(**i))
    return ResponseModel(response_code = status.HTTP_200_OK, message = "Success", payload = animeGenre)
    
@app.get("/anime/released/{anime_released_date}", tags = ["GET"])
async def anime(anime_released_date: str):
    animeReleaseDate = []
    animeResponse =  collection.find({'released': {'$regex': anime_released_date, '$options': 'i'}})
    async for i in animeResponse:
        animeReleaseDate.append(AnimeData(**i))
    if len(animeReleaseDate) > 0:
        return ResponseModel(response_code = status.HTTP_200_OK, message = "Success", payload = animeReleaseDate)
    else:
        return ResponseModel(response_code = status.HTTP_404_NOT_FOUND, message = f'Invalid year', payload = animeReleaseDate)


@app.get("/anime/status/{anime_status}", tags = ["GET"])
async def anime(anime_status: str):
    animeStatus = []
    animeResponse =  collection.find({'status': {'$regex': anime_status, '$options': 'i'}})
    async for i in animeResponse:
        animeStatus.append(AnimeData(**i))
    return ResponseModel(response_code = status.HTTP_200_OK, message = "Success", payload = animeStatus)

@app.get("/anime/category/{anime_category}", tags = ["GET"], status_code = status.HTTP_200_OK)
async def anime(anime_category: str):
    animeCategory = []
    animeResponse =  collection.find({'anime_type': {'$regex': anime_category, '$options': 'i'}})
    async for i in animeResponse:
        animeCategory.append(AnimeData(**i))
    return ResponseModel(response_code = status.HTTP_200_OK, message = "Success", payload = animeCategory)