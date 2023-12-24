# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 17:34:16 2023

@author: haris
"""

import pandas as pd
# from hello import res
import json
import requests
from db import politics_comments_collection, youtube_collection, politics_collection, yt_crime_collection, yt_politics_collection, comment_sentiment_collection, yt_crime_sentiment_collection
from authentication import headers
#import pytz
import io, urllib, base64
from datetime import datetime, timezone, timedelta
import time
import threading
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator
from collections import defaultdict
import pymongo
import numpy as np
from log_config import setup_logging
logger = setup_logging()

def sentimental_plot(min_score,max_score):
    # Fetch data from the collections
    senti_data = comment_sentiment_collection.find({})
    senti_youtube_data = yt_crime_sentiment_collection.find({})
    
    print(pymongo.__version__)
    '''negative_count = senti_data.count_documents({"sentiment_score": {"$lt": min_score}})+senti_youtube_data.count_documents({"sentiment_score": {"$lt": min_score}})
    neutral_count = senti_data.count_documents({"sentiment_score": {"$gte": min_score, "$lte": max_score}})+senti_youtube_data.count_documents({"sentiment_score": {"$gte": min_score, "$lte": max_score}})
    positive_count = senti_data.count_documents({"sentiment_score": {"$gt": max_score}})+senti_youtube_data.count_documents({"sentiment_score": {"$gt": max_score}})
    '''
    negative_count=0
    neutral_count=0
    positive_count=0
    for document in senti_data:
        try:
            sentiment_score=float(document.get('sentiment_score'))
        except:
            continue
        if sentiment_score is None:
            # Handle the case when sentiment_score is None (adjust as needed)
            #print("Skipping document with None sentiment_score")
            continue
        if sentiment_score<=min_score:
            negative_count=negative_count+1
        elif sentiment_score>min_score and sentiment_score<max_score:
            neutral_count=neutral_count+1
        elif sentiment_score>=max_score:
            positive_count=positive_count+1
            
    for document in senti_youtube_data:
        sentiment_score=document.get('sentiment')
        if sentiment_score is None:
            # Handle the case when sentiment_score is None (adjust as needed)
            #print("Skipping document with None sentiment_score")
            continue
        if sentiment_score<=min_score:
            negative_count=negative_count+1
        elif sentiment_score>min_score and sentiment_score<max_score:
            neutral_count=neutral_count+1
        elif sentiment_score>=max_score:
            positive_count=positive_count+1
    
    
    
    labels = ['Negative', 'Neutral', 'Positive']
    counts = [negative_count, neutral_count, positive_count]
    
    total_count = sum(counts)
    negative_percentage = (negative_count / total_count) * 100
    neutral_percentage = (neutral_count / total_count) * 100
    positive_percentage = (positive_count / total_count) * 100
    
    plt.bar(labels, counts, color=['red', 'grey', 'green'])
    plt.xlabel('Sentiment')
    plt.ylabel('Comment Count')
    plt.title('Sentiment Analysis')
    for i, count in enumerate(counts):
        percentage = (count / total_count) * 100
        plt.text(i, count + 0.1, f"{percentage:.2f}%", ha='center', va='bottom')
    
    img2 = io.BytesIO()
    plt.savefig(img2, format='png')
    img2.seek(0)
    sentimental_custom_data = urllib.parse.quote(base64.b64encode(img2.read()).decode())
    #plt.show()
    plt.close()
    return sentimental_custom_data
    #plt.show()

