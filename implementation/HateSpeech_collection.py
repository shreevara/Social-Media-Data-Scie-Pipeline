# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:00:21 2023

@author: haris
"""
import pymongo
import pandas as pd
# from hello import res
import json
import requests
from db import crime_collection, politics_collection, politics_comments_collection, dem_rep_toxicity_collection
from authentication import headers
import pytz
from datetime import datetime, timezone, timedelta
import time
import threading
from collections import Counter
import matplotlib.pyplot as plt
import re
df = pd.DataFrame()
from log_config import setup_logging
logger = setup_logging()

# try:
#     mongo = pymongo.MongoClient(
#         host="localhost",
#         port=27017,
#         serverSelectionTimeoutMS = 1000
#     )
#     db = mongo["Crawler"]
#     dem_rep_toxicity_collection=db["Politics_toxicity"]
#     mongo.server_info()
# except:
#     print("Error - Could not connect to the database")

#comment="I am a good guy"
def hs_check_comment(comment):
    CONF_THRESHOLD = 0.9
    
    data = {
      "token": "e08ea01337edf40f5f65facf5b93c94c",
      "text": comment
    }
    try:
        response = requests.post("https://api.moderatehatespeech.com/api/v1/moderate/", json=data).json()
    
    
        print("\nResponse:\n")
        print(response)
        return response["class"], response["confidence"]
    except Exception as e:
        logger.exception(f"Exception occured while hitting moderatehatespeech api: {e}")

   
        
    
def HateSpeech_insert(subreddit):   
    for subreddit in subreddits:
        republican_documents=politics_collection.find({"subreddit":subreddit})
        
        for document in republican_documents:
            comment_records = document.get("comment_records", {})
        
            for comment_id, comment_data in comment_records.items():
                existing_post = dem_rep_toxicity_collection.find_one({"_id":comment_id})
                if not existing_post:
                    comment_text = re.sub(r'[^A-Za-z0-9\s]', '', comment_data.get("body"))
                    print(comment_text)
                    if comment_text:
                        try:
                            time.sleep(3)
                            toxicity_class, toxicity_confidence=hs_check_comment(comment_text)
                            
                        # Create a new document with the transformed data
                            new_document = {
                                "_id": comment_id,
                                "subreddit": subreddit,
                                "comment_text": comment_text,
                                "toxicity_class":toxicity_class,
                                "toxicity_confidence":toxicity_confidence
                            }
                            dem_rep_toxicity_collection.insert_one(new_document)
                        except Exception as e:
                            logger.exception(f"Exception occured: {e}")

interval_minutes = 10
# Open the file in read mode
try:
    with open('hatespeech_subreddits', 'r') as file:
        # Read the lines from the file and remove newline characters
        subreddits = [line.strip() for line in file]
except Exception as e:
    logger.exception(f"exception occured while reading the file `hatespeech_subreddits`: {e}")

def threaded_periodic_task():
    while True:
        HateSpeech_insert(subreddits)
        time.sleep(interval_minutes * 60)
        
rthread = threading.Thread(target=threaded_periodic_task)
#ythread.daemon = True  # The thread will exit when the main program exits
rthread.daemon = True 
#ythread.start()
rthread.start()

# Keep the main program running (indefinitely) to allow the periodic task to continue
while True:
    pass
    




