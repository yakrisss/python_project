from datetime import datetime
import settings

collection = settings.collection
client = settings.mongo_db

def log_create(query_type, query_str):
    if collection is None:
        print("MongoDB is not connected — logging not performed")
        return
    doc = {
        "query_type": query_type,
        "query_str": query_str,
        "timestamp": datetime.now()
    }
    try:
        collection.insert_one(doc)
    except Exception as e:
        print(f"Error writing log to MongoDB: {e}")


def get_top_5_queries(n=5):
    if collection is None:
        print("MongoDB is not connected — cannot get top queries")
        return []
    pipeline = [
        {"$group": {"_id": "$query_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": n}
    ]
    try:
        return list(collection.aggregate(pipeline))
    except Exception as e:
        print(f"Ошибка при получении топ запросов: {e}")
        return []


def close():
    client.close()