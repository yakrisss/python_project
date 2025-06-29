from datetime import datetime
import settings
import logging


logger = logging.getLogger(__name__)


collection = settings.mongo_collection


def log_create(query_type, query_str):
    """
    Insert a log document into MongoDB collection.
    """
    if collection is None:
        logger.warning("MongoDB: collection is None — cannot write log")
        return

    doc = {
        "query_type": query_type,
        "query_str": query_str,
        "timestamp": datetime.now()
    }
    try:
        collection.insert_one(doc)
        logger.info(f"Log created for query_type={query_type}, query_str={query_str}")
    except Exception as e:
        logger.error(f"Error writing log to MongoDB: {e}")


def get_top_5_queries(n=5):
    """
    Retrieve top n queries grouped by type and query string.
    """
    if collection is None:
        logger.warning("MongoDB is not connected — cannot get top queries")
        return []

    pipeline = [
        {"$group": {
            "_id": {"query_type": "$query_type", "query_str": "$query_str"},
            "count": {"$sum": 1},
            "last_query": {"$max": "$timestamp"}
        }},
        {"$sort": {"count": -1, "last_query": -1}},
        {"$limit": n}
    ]

    try:
        return list(collection.aggregate(pipeline))
    except Exception as e:
        logger.error(f"Error retrieving top queries: {e}")
        return []


def print_top_5_queries(top_queries):
    """
    Print formatted top queries to console.
    """
    if not top_queries:
        print("No queries found.")
        return

    print("Top 5 most popular search queries:\n")
    for i, item in enumerate(top_queries, 1):
        qtype = item['_id']['query_type']
        qstr = item['_id']['query_str']
        count = item['count']
        print(f"{i}. Query type: {qtype}")
        print(f"   Keyword: \"{qstr}\"")
        