import pymysql
import pymongo


DATABASE_MYSQL = {
    'host': 'ich-db.edu.itcareerhub.de',
    'user': 'ich1',
    'password': 'password',
    'database': 'sakila',
    'charset': 'utf8mb4'
}

def connect_mysql():
    try:
        conn = pymysql.connect(**DATABASE_MYSQL)
        if conn.open:
            print("MySQL: connection established")
        else:
            print("MySQL: connection not open")
        return conn
    except Exception as e:
        print(f"MySQL: connection error — {e}")
        return None

MOVIE_RESULT_LIMIT = 10

DATABASE_MONGO = (
    "mongodb://ich_editor:verystrongpassword"
    "@mongo.itcareerhub.de/?readPreference=primary"
    "&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"
)


def connect_mongo():
    try:
        client = pymongo.MongoClient(DATABASE_MONGO)
        client.admin.command("ping")
        print("MongoDB: connection established")
        return client
    except Exception as e:
        print(f"MongoDB: connection error — {e}")
        return None

connection = connect_mysql() #проверка на подключение клиента для монго...подкобчение к курсору sql будет в db
client = connect_mongo()

if client:
    mongo_db = client["ich_edit"]
    collection = mongo_db["final_project_100125_hiunter"]
else:
    mongo_db = None
    collection = None