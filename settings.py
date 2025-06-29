import pymysql
import pymongo
import logging

logger = logging.getLogger(__name__)

DATABASE_MYSQL = {
    'host': 'ich-db.edu.itcareerhub.de',
    'user': 'ich1',
    'password': 'password',
    'database': 'sakila',
    'charset': 'utf8mb4'
}

DATABASE_MONGO = (
    "mongodb://ich_editor:verystrongpassword"
    "@mongo.itcareerhub.de/?readPreference=primary"
    "&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"
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


# --- Initialize connections at import time ---

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
