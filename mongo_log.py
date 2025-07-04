"""
Logs movie search queries to MongoDB and retrieves top queries.

Features:
- Log queries with type, string, and timestamp.
- Fetch top N frequent queries.
- Print formatted query statistics.

Depends on settings.mongo_collection and logging.
"""


import logging
from datetime import datetime
from typing import List, Dict, Any

from pymongo.errors import PyMongoError

import settings


logger = logging.getLogger(__name__)
collection = settings.mongo_collection


def log_create(query_type: str, query_str: str) -> None:
    """
    Insert a log document into the MongoDB collection.

    Args:
        query_type (str): The type/category of the query (e.g., 'film_name', 'actor').
        query_str (str): The query string that was searched.
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
        logger.info("Log created for query_type=%s, query_str=%s", query_type, query_str)
    except PyMongoError as e:
        logger.error("Some error happened: %s", e)


def get_top_5_queries(n: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve the top n most frequent queries from MongoDB logs, grouped by query type and string.

    Args:
        n (int): Number of top queries to retrieve. Defaults to 5.

    Returns:
        List[Dict[str, Any]]: A list of documents with fields:
            - '_id': {'query_type': str, 'query_str': str}
            - 'count': int (number of occurrences)
            - 'last_query': datetime (timestamp of last query)
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
    except PyMongoError as e:
        logger.error("Error happened: %s", e)
        return []
