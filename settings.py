import pymysql
import pymongo
import logging
from dotenv import load
import os


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

MOVIE_RESULT_LIMIT = 10


def connect_mysql():
    try:
        conn = pymysql.connect(**DATABASE_MYSQL)
        if conn.open:
            return conn
    except Exception as e:
        raise ConnectionError(f"MySQL connection error: {e}")


def connect_mongo():
    try:
        client = pymongo.MongoClient(DATABASE_MONGO)
        client.admin.command("ping")
        return client
    except Exception as e:
        raise ConnectionError(f"MongoDB connection error: {e}")


def get_mongo_collection(client):
    """
    Return collection from MongoDB: database 'ich_edit', collection 'final_project_100125_hiunter'.
    """
    if client:
        db = client["ich_edit"]
        return db["final_project_100125_hiunter"]
    else:
        logger.warning("MongoDB: client is None — cannot get collection")
        return None

#запуск соединения
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
