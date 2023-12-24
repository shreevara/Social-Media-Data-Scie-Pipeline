from db import source_collection
from log_config import setup_logging
logger = setup_logging()

crime_subreddits = ['r/TrueCrime','r/SerialKillers','r/CrimeScene','r/RedditCrimeCommunity']
political_subreddits = ['r/Republican','r/democrats','r/Ask_Politics','r/politics','r/PoliticalDiscussion']
youtube_channel_ids = {
    "UCupvZG-5ko_eiXAupbDfxWw" : "CNN News", 
    "UCP6HGa63sBC7-KHtkme-p-g" : "US TODAY", 
    "UCHd62-u_v4DvJ8TCFtpi4GA" : "WashingtonPost",  
    "UCeY0bbntWzzVIaj2z3QigXg" : "NBC News", 
    "UC69uYUqvx-vw4luuX7aHNLQ" : "True crime daily", 
    "UCXIJgqnII2ZOINSWNOGFThA" : "Fox news", 
    "UCBi2mrWuNuyYy4gbM6fU18Q" : "ABC", 
    "UC8p1vwvWtl6T73JiExfWs1g" : "CBS", 
    "UCEXGDNclvmg6RW0vipJYsTQ" : "Channels Television", 
    "UChLtXXpo4Ge1ReTEboVvTDg" : "Global News"
}

try:
    if not source_collection.find_one({"_id": "jeremy"}):
        source_collection.insert_one({
            "_id" : "jeremy",
            "crime_subreddits" : crime_subreddits,
            "political_subreddits" : political_subreddits,
            "youtube_channel_ids" : youtube_channel_ids
        })
    source_data = source_collection.find_one({"_id" : "jeremy"})
    logger.info("Initialization of the DB with crime_subreddits, political_subreddits, youtube_channel_ids done!!")
except Exception as e:
    logger.exception(f"Exception occured while inserting data into DB for initialization: {e}")

# print(source_data)
# for i in source_data:
#     source_crime_subreddits = i["crime_subreddits"]
#     source_political_subreddits = i["political_subreddits"]
#     source_youtube_channel_ids = i["youtube_channel_ids"]
# print(source_crime_subreddits)
# print(source_political_subreddits)
# print(source_youtube_channel_ids)

# for channel_id, channel_name in source_youtube_channel_ids.items():
#         print(channel_id, channel_name)

def update_crime_subreddit(subreddit):
    try:
        if not source_collection.find_one({"crime_subreddits" : {"$regex":subreddit,"$options":"i"}}):
            source_collection.update_one({"_id":"jeremy"}, {"$push": {"crime_subreddits" : subreddit}})
            source_data = source_collection.find_one({"_id" : "jeremy"})
            return "crime_subreddit_added"
        else:
            return "subreddit_already_added"
    except Exception as e:
        logger.exception(f"Exception occured while updating the crime subreddit data: {e}")
        return "Exception occured!! please check the log"

def update_political_subreddit(subreddit):
    try:
        if not source_collection.find_one({"political_subreddits" : subreddit}):
            source_collection.update_one({"_id":"jeremy"}, {"$push": {"political_subreddits" : subreddit}})
            source_data = source_collection.find_one({"_id" : "jeremy"})
            return "politics_subreddit_added"
        else:
            return "subreddit_already_added"
    except exception as e:
        logger.exception(f"Exception occured while updating the politics subreddit data: {e}")
        return "Exception occured!! please check the log"


def insert_channel_ids(channel_name, channel_id):
    try:
        if not source_collection.find_one({"youtube_channel_ids."+channel_id : {"$exists" : True}}):
            source_collection.update_one({"_id":"jeremy"}, {"$set": {"youtube_channel_ids."+channel_id : channel_name}})
            source_data = source_collection.find_one({"_id" : "jeremy"})
            return "channel "+channel_name+" added"
        return "channel_already_added"
    except Exception as e:
        logger.exception(f"Exception occured while updating channel ids in youtube source data: {e}")
        return "Exception occured!! please check the log"