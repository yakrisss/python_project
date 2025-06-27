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


def get_top_5_queries(n=5):  # Группировка по типу и ключевому слову
    if collection is None:
        print("MongoDB is not connected — cannot get top queries")
        return []
    pipeline = [{"$group": {"_id": {"query_type": "$query_type",
                    "query_str": "$query_str"}, #группировка по типу запрос аи по ключевому слову
                "count": {"$sum": 1},
                "last_query": {"$max": "$timestamp"}}},
        {"$sort": {"count": -1, "last_query": -1}},
        {"$limit": n}
    ]
    try:
        return list(collection.aggregate(pipeline))
    except Exception as e:
        print(f"Ошибка при получении топ запросов: {e}")
        return []


def print_top_5_queries(top_queries):
    if not top_queries:
        print("No queries found.")
        return
        
    print("Top 5 most popular search queries: \n")
    for i, item in enumerate(top_queries, 1):
        qtype = item['_id']['query_type']
        qstr = item['_id']['query_str']
        count = item['count']
        print(f"{i}. Query type: {qtype}")
        print(f"   Keyword: \"{qstr}\"")
        print(f"   Number of searches: {count}")
        

def close():
    client.close()