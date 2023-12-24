from db import youtube_collection, source_collection
import os
import json
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from datetime import datetime
import pytz
import threading
import time
from datetime import date, timedelta
from init_db import source_data
from log_config import setup_logging
logger = setup_logging()


# Set the US Eastern Time (ET) timezone
us_eastern_timezone = pytz.timezone("US/Eastern")

# Define the current date and time in the US Eastern Time (ET) timezone
current_datetime = datetime.now(us_eastern_timezone)
current_date = current_datetime.strftime("%Y-%m-%d")


# Replace with your own API key
API_KEY = "AIzaSyClSieuBDGzPkQm-PSezfWosJe7FbLnipQ"

# Load the JSON file with channel names and IDs, if it exists
channel_data = {}
# if os.path.exists("channel_ids.json"):
#     with open("channel_ids.json", "r") as file:
#         channel_data = json.load(file)

source_data = source_collection.find_one({"_id" : "jeremy"})
# for i in source_data:
channel_data = source_data["youtube_channel_ids"]

# Initialize data as an empty list
data_for_all_channels = []

# Check if the output file exists
if os.path.exists("output.json"):
    try:
        # Load existing data from the output file
        with open("output.json", "r", encoding="utf-8") as file:
            data_for_all_channels = json.load(file)
    except json.JSONDecodeError:
        # Handle the case where the file is empty or contains invalid JSON
        data_for_all_channels = []

# Initialize a dictionary to keep track of video IDs for which comments have been added
added_comments_videos = {}

# Set up the YouTube Data API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

# Function to get top 10 videos of today based on view count
def get_top_videos(channel_id, channel_name):
    top_videos = []

    try:
        # Use the current_date variable for date filtering in your API request
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=10,
            order="viewCount",
            type="video",
            publishedAfter=f"{current_date}T00:00:00Z",  # Videos published on the current date in US Eastern Time (ET)
            publishedBefore=f"{current_date}T23:59:59Z"
        )
        response = request.execute()

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            video_description, video_date, view_count = get_video_details(video_id)
            top_comments = get_top_comments(video_id)

            # Check if the video ID already exists in the data
            # existing_channel_data = next((c for c in data_for_all_channels if c["channel_id"] == channel_id), None)

            existing_channel_data_db = youtube_collection.find_one({"channel_id" : channel_id})
            # print(existing_channel_data_db)

            if existing_channel_data_db:
                # Check if the video ID exists within the channel data
                existing_video = next((v for v in existing_channel_data_db["top_videos"] if v["video_id"] == video_id), None)


                # existing_video_db = youtube_collection.find_one({"channel_id" : channel_id, "top_videos": {"$elemMatch":{"video_id":video_id}}})

                if existing_video:
                    # Check if the comment is not already in the list before appending it
                    # youtube_collection.update_one({"channel_id" : channel_id, "top_videos.video_id":video_id},{"$push":{"top_videos.$.top_comments":"Hey there, Gopi here!"}})
                    # comment_db = youtube_collection.find_one({"channel_id" : channel_id, "top_videos": {"$elemMatch":{"video_id":video_id, "top_comments": comment}}}}})
                    for comment in top_comments:
                        if comment not in existing_video["top_comments"]:
                            # existing_video["top_comments"].append(comment)
                            youtube_collection.update_one({"channel_id" : channel_id, 
                                                        "top_videos.video_id":video_id},
                                                        {"$push":{"top_videos.$.top_comments":comment}}
                                                        )
                else:
                    # Add new video details to the channel data
                    # existing_channel_data["top_videos"].append({
                    #     "video_id": video_id,
                    #     "title": video_title,
                    #     "description": video_description,
                    #     "date": video_date,
                    #     "view_count": view_count,
                    #     "top_comments": top_comments
                    # })
                    youtube_collection.update_one({
                        "channel_id":channel_id,
                    },{
                        "$push":{
                            "top_videos":{
                                "video_id": video_id,
                                "title": video_title,
                                "description": video_description,
                                "date": video_date,
                                "view_count": view_count,
                                "top_comments": top_comments
                            }
                        }
                    })
            else:
                # Add new channel data along with the new video details
                # data_for_all_channels.append({
                #     "channel_name": channel_name,
                #     "channel_id": channel_id,
                #     "top_videos": [{
                #         "video_id": video_id,
                #         "title": video_title,
                #         "description": video_description,
                #         "date": video_date,
                #         "view_count": view_count,
                #         "top_comments": top_comments
                #     }]
                # })
                youtube_collection.insert_one({
                    "channel_name": channel_name,
                    "channel_id": channel_id,
                    "top_videos": [{
                        "video_id": video_id,
                        "title": video_title,
                        "description": video_description,
                        "date": video_date,
                        "view_count": view_count,
                        "top_comments": top_comments
                    }]
                })
    except Exception as e:
        logger.exception(f"Execption occured while inserting doc in yt collection for {channel_name}: {e}")
    return top_videos

# Function to get video details (description, date, view count)
def get_video_details(video_id):
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id,
        )
        response = request.execute()
        item = response.get("items", [])[0]

        video_description = item["snippet"]["description"]
        video_date = item["snippet"]["publishedAt"]
        view_count = item["statistics"]["viewCount"]

        return video_description, video_date, view_count
    exception Exception as e:
        logger.exception(f"Exception occured while getting video details for video_id={video_id}:{e}")

# Function to get top 100 comments for a video based on like count
def get_top_comments(video_id):
    top_comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100,
            order="relevance",  # Sort by relevance to get top comments
        )
        response = request.execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            top_comments.append(comment)

    except HttpError as e:
        logger.exception(f"An error occurred while getting top_comments fro video_id:{video_id}: {e}")

    return top_comments

# Function to be called periodically (e.g., every hour)
def periodic_task():
    print("Running periodic task...")
    
    for channel_id, channel_name in channel_data.items():
        get_top_videos(channel_id, channel_name)

    # # Save the updated data to the output file
    # with open("output.json", "w", encoding="utf-8") as file:
    #     json.dump(data_for_all_channels, file, ensure_ascii=False, indent=4)

    print(f"Top 10 videos and top 100 comments for all channels have been updated in 'output.json'.")

# # Define the interval for running the periodic task (e.g., 1 hour)
# interval_hours = 6
# # Create a threading timer to run the periodic task
# def threaded_periodic_task():
#     while True:
#         periodic_task()
#         time.sleep(interval_hours * 3600)  # Sleep for the specified interval

# # Start the threaded periodic task
# thread = threading.Thread(target=threaded_periodic_task)
# thread.daemon = True  # The thread will exit when the main program exits
# thread.start()

# # Keep the main program running (indefinitely) to allow the periodic task to continue
# while True:
#     pass
