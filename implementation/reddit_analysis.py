import pandas as pd
# from hello import res
import json
import requests
from db import crime_collection, politics_collection, source_collection
from authentication import headers
import pytz
from datetime import datetime, timezone
from datetime import date, timedelta
from init_db import source_data
from log_config import setup_logging
logger = setup_logging()


df = pd.DataFrame()
est = pytz.timezone("US/Eastern")
utc = pytz.utc

source_crime_subreddits = source_data["crime_subreddits"]
source_political_subreddits = source_data["political_subreddits"]

print("---------------------INSIDE REDDIT_ANALYSIS------------------------")

def insert_into_collection(subreddits, collection):
    try:
        for sub in subreddits:
            res = requests.get(f'https://oauth.reddit.com/{sub}/new', headers=headers, params={'limit':'100'})
            print(len(res.json()['data']['children']))
            for i in res.json()['data']['children']:
                idx=i['data']['id']
                existing_post = collection.find_one({"_id":idx})
                res1 = requests.get(f'https://oauth.reddit.com/{sub}/comments/{idx}', 
                        headers=headers)
                df1=pd.DataFrame()
                print("=============================================================================")
                # print(res1.json())
                print(i['data']['title'])
                print(len(res1.json()[1]['data']['children']))
                print("=============================================================================")
                count=0
                if not existing_post:
                    try:
                        post_created_at = datetime.utcfromtimestamp(i['data']['created_utc']).replace(tzinfo=utc)
                        collection.insert_one({
                            '_id':i['data']['id'],
                            'subreddit':i['data']['subreddit'],
                            'title':i['data']['title'],
                            'author':i['data']['author'],
                            'selftext':i['data']['selftext'],
                            'postedtime(est)':post_created_at.astimezone(est),
                            'comment_records':{}
                        })
                        existing_post = collection.find_one({"_id":idx})
                    except Exception as e:
                        print(e)
                for j in res1.json()[1]['data']['children']:
                    count= count+1
                    # if hasattr(j['data'],'body'):
                    #     print(True)
                    idx1=j['data']['id']
                    if idx1 not in existing_post['comment_records'].keys():
                        try:
                            # print(comment_created_at.astimezone(est))
                            collection.update_one({"_id":i["data"]["id"]},{"$set":{f"comment_records.{idx1}":{
                                'body':j['data']['body'],
                                'author':j['data']['author']
                            }}})
                            # df1 = df1._append({
                            #     'body':j['data']['body'],
                            #     'c_id':j['data']['id'],
                            #     'author':j['data']['author']
                            # }, ignore_index=True)
                        except:
                            pass
                    # print(df1)
                # records1 = list(json.loads(df1.T.to_json()).values())
                    # print(df1)
                    # records1 = list(json.loads(df1.T.to_json()).values())
                    # post_created_at = datetime.utcfromtimestamp(i['data']['created_utc']).replace(tzinfo=utc)
                    # df = df._append({
                    #     '_id':i['data']['id'],
                    #     'subreddit':i['data']['subreddit'],
                    #     'title':i['data']['title'],
                    #     'author':i['data']['author'],
                    #     'selftext':i['data']['selftext'],
                    #     'postedtime(est)':post_created_at.astimezone(est),
                    #     'comment_records':records1,
                    # }, ignore_index=True)            
    except Exception as e:
        logger.exception(f"Exception occured while retrieving and processing data from reddit API: {e}")
        # print(e)

def collect_new_crime_data():
    # crime_subreddits = ['r/TrueCrime','r/SerialKillers','r/CrimeScene','r/RedditCrimeCommunity']
    df = pd.DataFrame()
    # records=[]
    insert_into_collection(source_crime_subreddits, crime_collection)
    logger.info("collection of crime subreddit records done!!")

def collect_new_political_data():
    # political_subreddits = ['r/Republican','r/democrats','r/Ask_Politics','r/politics','r/PoliticalDiscussion']
    df = pd.DataFrame()
    # records=[]
    insert_into_collection(source_political_subreddits, politics_collection)
    # records = json.loads(df.T.to_json()).values()
    logger.info("collection of politics subreddit records done!!")