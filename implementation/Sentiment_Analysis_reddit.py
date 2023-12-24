import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
from db import politics_collection,crime_collection, youtube_collection,comment_sentiment_collection
import pandas as pd
from log_config import setup_logging
logger = setup_logging()
# Download the VADER lexicon
nltk.download('vader_lexicon')

def clean_text(text):
    # Remove HTML tags and special characters
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def preprocess_text(text):
    cleaned_text = clean_text(text)
    return cleaned_text

def perform_sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    
    # Get sentiment polarity scores
    sentiment_scores = sia.polarity_scores(text)
    
    # Determine sentiment category based on compound score
    compound_score = sentiment_scores['compound']
    
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def reddit_sentiment(collection):
# Fetch documents from MongoDB
    documents = collection.find()  
    comments=[]
    sentiments=[]
    '''for document in cursor:
        subreddit = document["subreddit"]
        
        # Iterate through comment records
        for comment_id, comment_data in document["comment_records"].items():
            comment_sources.append("Reddit")
            comment_subreddits.append(subreddit)
            comment_texts.append(comment_data["body"])'''
    
    # Perform sentiment analysis on title and description for each document
    for document in documents:
        #title = document.get("title", "")
        #description = document.get("description", "")
        for comment_id, comment_data in document["comment_records"].items():
            existing_post = comment_sentiment_collection.find_one({"_id":comment_id})
        # Combine title and description for sentiment analysis
            if not existing_post:
                text_to_analyze = comment_data["body"]
                #print(text_to_analyze)
                # Preprocess the text
                preprocessed_text = preprocess_text(text_to_analyze)
                
                # Perform sentiment analysis
                sentiment = perform_sentiment_analysis(preprocessed_text)
                record={
                    "_id":comment_id,
                    "comment":text_to_analyze,
                    "collection_name":collection.name,
                    "sentiment":sentiment
                    }
                comment_sentiment_collection.insert_one(record)
            
try:
    df_reddit_crime=reddit_sentiment(crime_collection)
    df_reddit_politics=reddit_sentiment(politics_collection)
except Exception as e:
    logger.exception(f"Exception occured!: {e}")

