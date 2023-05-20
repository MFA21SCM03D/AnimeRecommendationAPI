import urllib
import pymongo
import certifi
import motor.motor_asyncio

# Using urllib to escape the password from the url and to use the password value.
# Certifi to bypass the SSL error and the connection is se to the primary cluster node using readPreference=primary.
# Motor is mongodb driver for python which is much easier to use.

mongoURL = 'mongodb+srv://mayurdeshmukh2442:' + urllib.parse.quote("mongoDB@123") + '@fastapi.yqk7twe.mongodb.net/'

try:
    # connection = pymongo.MongoClient(mongoURL+ "?retryWrites=true&w=majority&readPreference=primary", tlsCAFile=certifi.where(), serverSelectionTimeoutMS=1)
    connection = motor.motor_asyncio.AsyncIOMotorClient(mongoURL+ "?retryWrites=true&w=majority&readPreference=primary", tlsCAFile=certifi.where(), serverSelectionTimeoutMS=1)
    db = connection["AnimeDatabase"]
    collection = db["Anime"]
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)
