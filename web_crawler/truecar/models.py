"""Module containing functions to connect to MongoDB."""

import pymongo 
from scrapy.utils.project import get_project_settings

def db_connect():
    """Connects to MongoDB database."""
    client = pymongo.MongoClient(get_project_settings().get("MONGO_URI"))
    db = client.vehicles

    return db 