from db import crime_collection, politics_collection, youtube_collection, politics_comments_collection, source_collection, yt_crime_collection, yt_politics_collection
from log_config import setup_logging
import pandas as pd


logger = setup_logging()


try:
    crime_dataset = crime_collection.find()
    politics_dataset = politics_collection.find()
    yt_crime_dataset = yt_crime_collection.find()
    yt_politics_dataset = yt_politics_collection.find()
except Exception as e:
    logger.exception(f"An exception occured while retrieving data from DB: {e}")
logger.info("Collected data from DB")

def reddit_dataset(dataset):
    output_reddit_list = []
    try:
        for data in dataset:
            output_reddit_list.append({"subreddit":data["subreddit"], "title":data["title"], "author": data["author"], "posted_time":data["postedtime(est)"], "no_of_comments":len(data["comment_records"].keys())})
    except Exception as e:
        logger.exception(f"Exception occured while processing data from reddit dataset: {e}")
    return output_reddit_list

def yt_dataset(dataset):
    output_yt_list = []
    try:
        for data in dataset:
            video = data["top_videos"][0]
            output_yt_list.append({"channel_name": data["channel_name"], "channel_id": data["channel_id"], "video_id": video["video_id"],
            "title":video["title"], "posted_time": video["date"], "no_of_comments": len(video["top_comments"])})
    except Exception as e:
        logger.exception(f"Exception occured while processing data from youtube dataset: {e}")
    return output_yt_list

crime_list = reddit_dataset(crime_dataset)
politics_list = reddit_dataset(politics_dataset)

yt_crime_list = yt_dataset(yt_crime_dataset)
yt_politics_list = yt_dataset(yt_politics_dataset)

def dataset_table_reddit(reddit_list):
    df = pd.DataFrame(reddit_list)
    df['posted_time'] = pd.to_datetime(df['posted_time'])
    result_df = df.groupby('subreddit').agg(
        Posts=pd.NamedAgg(column='title', aggfunc='count'),
        Authors=pd.NamedAgg(column='author', aggfunc='nunique'),
        Comments=pd.NamedAgg(column='no_of_comments', aggfunc=lambda y: sum(y)),
        Min_Max_Date=pd.NamedAgg(column='posted_time', aggfunc=lambda x: f"{x.min().strftime('%m/%d')} - {x.max().strftime('%m/%d')}")
    )
    result_df=result_df.sort_values(by=["Posts"], ascending=False)
    total_row = pd.DataFrame({
    'Posts': [result_df['Posts'].sum()],
    'Authors': [result_df['Authors'].sum()],
    'Comments': [result_df['Comments'].sum()],
    'Min_Max_Date': [f"{result_df['Min_Max_Date'].min().split(' - ')[0]} - {result_df['Min_Max_Date'].max().split(' - ')[1]}"]
    }, index=['All'])
    result_df = result_df._append(total_row)
    result_df.index.name = 'subreddit'
    return result_df

def dataset_table_youtube(youtube_list):
    df = pd.DataFrame(youtube_list)
    df['posted_time'] = pd.to_datetime(df['posted_time'])
    result_df = df.groupby('channel_name').agg(
        Videos=pd.NamedAgg(column='title', aggfunc='count'),
        Comments=pd.NamedAgg(column='no_of_comments', aggfunc=lambda y: sum(y)),
        Min_Max_Date=pd.NamedAgg(column='posted_time', aggfunc=lambda x: f"{x.min().strftime('%m/%d')} - {x.max().strftime('%m/%d')}")
    )
    result_df=result_df.sort_values(by=["Videos"], ascending=False)
    total_row = pd.DataFrame({
        'Videos': [result_df['Videos'].sum()],
        'Comments': [result_df['Comments'].sum()],
        'Min_Max_Date': [f"{result_df['Min_Max_Date'].min().split(' - ')[0]} - {result_df['Min_Max_Date'].max().split(' - ')[1]}"]
    }, index=['All'])
    result_df = result_df._append(total_row)
    result_df.index.name = 'channel_name'
    return result_df

try:
    print("\n")
    print("-------------------REDDIT CRIME DATASET STATS-----------------------\n")
    print(dataset_table_reddit(crime_list))
    print("\n")
    print("-------------------REDDIT POLITICS DATASET STATS--------------------\n")
    print(dataset_table_reddit(politics_list))
    print("\n")
    print("-------------------YOUTUBE CRIME DATASET STATS----------------------\n")
    print(dataset_table_youtube(yt_crime_list))
    print("\n")
    print("-------------------YOUTUBE POLITICS DATASET STATS-------------------\n")
    print(dataset_table_youtube(yt_politics_list))
except Exception as e:
    logger.exception(f"Exception occured while processing DB data for stats: {e}")

