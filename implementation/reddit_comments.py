# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 10:35:42 2023

@author: haris
"""

import pandas as pd
# from hello import res
import json
import requests
from db import crime_collection, politics_collection, politics_comments_collection
from authentication import headers
import pytz
from datetime import datetime, timezone
from datetime import date, timedelta
import time
import threading
from log_config import setup_logging
logger = setup_logging()
df = pd.DataFrame()
est = pytz.timezone("US/Eastern")
utc = pytz.utc
print("---------------------INSIDE REDDIT_ANALYSIS------------------------")

start_time = int(time.time()) - 60
num_comments=0
def collect_reddit_comments(collection):
    num_comments=0
    try:
        subreddits = 'r/politics'
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        res = requests.get(f'https://oauth.reddit.com/{subreddits}/comments/', headers=headers, params={'limit':'100'})
        print(len(res.json()['data']['children']))
        comments=res.json()['data']['children']
        try:
            for i in res.json()['data']['children']:
                idx=i['data']['id']
                #print(idx)
                existing_post = collection.find_one({"_id":idx})
                if not existing_post:
                    existing_post = collection.find_one({"_id":idx})
                    post_created_at = datetime.utcfromtimestamp(i['data']['created_utc']).replace(tzinfo=utc)
                    collection.insert_one({
                        '_id':i['data']['id'],
                        'author':i['data']['author'],
                        'postedtime(est)':post_created_at.astimezone(est),
                        
                    })
                
        #comments_data = res.json()
        #comments_in_last_hour =  sum(comments_data["data"]["num_comments"] for item in comments_data["data"]["children"])
        except Exception as e:
            logger.exception(f"exception occured!: {e}")
        
    except Exception as e:
        logger.exception(f"exception occured!: {e}")


interval_minutes = 4
def threaded_periodic_task():
    while True:
        collect_reddit_comments(politics_comments_collection)
        time.sleep(interval_minutes * 60)
        
rthread = threading.Thread(target=threaded_periodic_task)
#ythread.daemon = True  # The thread will exit when the main program exits
rthread.daemon = True 
#ythread.start()
rthread.start()

# Keep the main program running (indefinitely) to allow the periodic task to continue
while True:
    pass

        
