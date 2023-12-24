import pymongo
from log_config import setup_logging
logger = setup_logging()

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo["Crawler"]
    crime_collection = db["Crime"]
    politics_collection = db["Politics"]
    youtube_collection = db["Newsinfo"]
    politics_comments_collection=db["pol_comments"]
    source_collection = db["sources_for_data"]
    yt_crime_collection = db["yt_crime"]
    yt_politics_collection = db["yt_politics"]
    comment_sentiment_collection = db["Comments_sentiments"]
    yt_crime_sentiment_collection = db["Youtube_Crime_Sentiments"]
    dem_rep_toxicity_collection=db["Politics_toxicity"]
    mongo.server_info()
except Exception as e:
    logger.exeption(f"Error - Could not connect to the database: {e}")