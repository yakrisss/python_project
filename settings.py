"""
Configuration settings for the application:
- MySQL and MongoDB connection parameters
- Movie search result limit
- Other global settings
"""


import os
import logging

import pymysql
import pymongo
from dotenv import load_dotenv

from pymysql.connections import Connection
from pymongo import MongoClient
from pymongo.collection import Collection


load_dotenv()

logger = logging.getLogger(__name__)


DATABASE_MYSQL = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': 'sakila',
    'charset': 'utf8mb4'
}


MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_DB = os.getenv('MONGO_DB')

DATABASE_MONGO = (
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/"
    f"?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource={MONGO_DB}"
)


# Limit for the number of movies returned per query
MOVIE_RESULT_LIMIT = 10


def connect_mysql() -> Connection:
    """
    Create and return a MySQL connection using pymysql.
    
    Returns:
        pymysql.connections.Connection if connection succeeds,
        None otherwise (raises ConnectionError).
    
    Raises:
        ConnectionError: if connection cannot be established.
    """
    try:
        conn = pymysql.connect(**DATABASE_MYSQL)
        if conn.open:
            return conn
        raise ConnectionError("MySQL connection is not open")
    except Exception as e:
        raise ConnectionError(f"MySQL connection error: {e}") from e


def connect_mongo() -> MongoClient:
    """
    Create and return a MongoDB client.
    
    Returns:
        pymongo.MongoClient if connection succeeds,
        None otherwise (raises ConnectionError).
    
    Raises:
        ConnectionError: if connection cannot be established.
    """
    try:
        client = pymongo.MongoClient(DATABASE_MONGO)
        client.admin.command("ping")
        return client
    except Exception as e:
        raise ConnectionError(f"MongoDB connection error: {e}") from e


def get_mongo_collection(client: MongoClient) -> Collection | None:
    """
    Return MongoDB collection from database 'ich_edit', collection 'final_project_100125_hiunter'.
    
    Args:
        client: pymongo.MongoClient instance or None
    
    Returns:
        pymongo.collection.Collection if client is valid,
        None otherwise.
    """
    if client:
        return client["ich_edit"]["final_project_100125_hiunter"]

    logger.warning("MongoDB: client is None — cannot get collection")
    return None


# establish connections on module import
try:
    mysql_connection = connect_mysql()
except ConnectionError as e:
    logger.error(e)
    mysql_connection = None

try:
    mongo_client = connect_mongo()
    mongo_collection = get_mongo_collection(mongo_client)
except ConnectionError as e:
    logger.error(e)
    mongo_client = None
    mongo_collection = None
