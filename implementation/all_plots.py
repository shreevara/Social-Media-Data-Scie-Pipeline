# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 09:36:11 2023

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
data2 = youtube_collection.find({})
comment_counts_by_date = defaultdict(int)

for entry in data2:
    for video in entry["top_videos"]:
        # Extract date from the timestamp
        date1 = datetime.strptime(video["date"], "%Y-%m-%dT%H:%M:%SZ").date()
        # Count the number of comments
        comment_count = len(video["top_comments"])
        #print(comment_count)
        # Aggregate comment counts by date
        comment_counts_by_date[date1] += comment_count

# Create lists for plotting
dates_plot = list(comment_counts_by_date.keys())
comment_counts = list(comment_counts_by_date.values())

# Plot the line graph
plt.plot(dates_plot, comment_counts, marker='o')
plt.xlabel('Date')
plt.ylabel('Number of Comments')
plt.title('Number of Comments for Each Video on a Given Day')
plt.xticks(rotation=45)
plt.tight_layout()

img3 = io.BytesIO()
plt.savefig(img3, format = 'png')
img3.seek(0)
yt_comments_data = urllib.parse.quote(base64.b64encode(img3.read()).decode())

plt.close()
#plt.show(block=True)







# Query the collection and process the data
yt_data = youtube_collection.find({})
comment_data = []
max_comments_per_day = {}

for entry in yt_data:
    for video in entry["top_videos"]:
        # Extract date from the timestamp
        date2 = datetime.strptime(video["date"], "%Y-%m-%dT%H:%M:%SZ").date()
        # Count the number of comments
        comment_count = len(video["top_comments"])
        # Append data for each video to the list
        comment_data.append({"date": date2, "comment_count": comment_count, "video_id": video["video_id"], "title": video["title"], "description": video["description"]})
        
        # Update max_comments_per_day if current video has more comments
        if date2 not in max_comments_per_day or comment_count > max_comments_per_day[date2]["comments"]:
            max_comments_per_day[date2] = {
                "video_id": video["video_id"],
                "title": video["title"],
                "description": video["description"],
                "comments": comment_count
            }

# Create lists for plotting
dates = [item["date"] for item in comment_data]
comment_counts1 = [item["comment_count"] for item in comment_data]

# Plot the line graph

plt.xlabel('Date')
plt.ylabel('Number of Comments')
plt.title('Number of Comments for Each Video on a Given Day')
plt.xticks(rotation=45)
plt.tight_layout()
plt.plot(dates, comment_counts1, marker='o', linestyle='None')

# Save the plot as an image
img2 = io.BytesIO()
plt.savefig(img2, format='png')
img2.seek(0)
yt_per_video_comments_data = urllib.parse.quote(base64.b64encode(img2.read()).decode())
plt.close()
# Show the plot
#plt.show()

# Print information about the video with the highest comments for each day
'''print("Maximum Comments for Each Day:")
for date, info in max_comments_per_day.items():
    print("***********************************\n")
    print(f"Date: {date}")
    print("Video ID:", info["video_id"])
    print("Title:", info["title"])
    #print("Description:", info["description"])
    print("Number of Comments:", info["comments"])
    print("-" * 30)'''








# Query data from MongoDB
data = list(politics_comments_collection.find({"postedtime(est)": {"$gte": datetime.fromisoformat("2023-11-01"), "$lt": datetime.fromisoformat("2023-11-15") }}))

# Convert data to DataFrame
df = pd.DataFrame(data)

# Convert "postedtime(est)" to datetime format
df["postedtime(est)"] = pd.to_datetime(df["postedtime(est)"])

# Set the date range (1st November to 14th November)
start_date = datetime(2023, 11, 1)
end_date = datetime(2023, 11, 14, 23, 59, 59)

# Create bins hourly
date_bins = pd.date_range(start=start_date, end=end_date, freq='H')

# Plot the graph
plt.figure(figsize=(30, 12))
plt.hist(df["postedtime(est)"], bins=date_bins, edgecolor='black', alpha=0.7)
plt.title('Number of Posts per Hour')
plt.xlabel('Date and Hour')
plt.ylabel('Number of Posts')
plt.xticks(rotation=45)
plt.tight_layout()

img2 = io.BytesIO()
plt.savefig(img2, format = 'png')
img2.seek(0)
pol_comments_data = urllib.parse.quote(base64.b64encode(img2.read()).decode())


#plt.show()

plt.close()


df = pd.DataFrame()

start_date = datetime(2023, 11, 1)
end_date = datetime(2023, 11, 15) 
#target_date = "2023-11-11"
#cursor = politics_comments_collection.find()
cursor = politics_collection.find({
    "postedtime(est)": {"$gte": start_date, "$lt": end_date},
    "subreddit":"politics"
})
# Initialize a Counter to count comments for each minute
comments_counter = Counter()

# Iterate through the documents and count comments per minute
for document in cursor:
    posted_time = document.get("postedtime(est)")
    
    if posted_time:
        # Convert posted_time to a Python datetime object
        #posted_time = datetime.fromisoformat(posted_time)
        # Extract minute-level information (you can also include seconds for more precision)
        day = posted_time.strftime("%Y-%m-%d")
        comments_counter[day] += 1
# Separate the data into x (timestamps) and y (comment counts)
'''x = list(comments_counter.keys())
y = list(comments_counter.values())'''
# Sort the data by timestamp (x-axis)
sorted_data = sorted(comments_counter.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))

# Separate the data into x (timestamps) and y (comment counts)
x, y = zip(*sorted_data)

# Plot the data as a bar graph
plt.figure(figsize=(12, 6))
plt.bar(x, y, color='skyblue')
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Comment Count")
plt.title("Number of Posts Per Day (Nov 1, 2023 - Nov 14, 2023)")
plt.tight_layout()

#plt.show()

img1 = io.BytesIO()
plt.savefig(img1, format = 'png')
img1.seek(0)
politics_posts_data = urllib.parse.quote(base64.b64encode(img1.read()).decode())

plt.close()


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo["Crawler"]
    dem_rep_toxicity_collection=db["Politics_toxicity"]
    mongo.server_info()
except:
    print("Error - Could not connect to the database")




data = dem_rep_toxicity_collection.find()
# Process data to create a suitable dataset for plotting
toxicity_counts = {"normal": {}, "flag": {}}

for entry in data:
    subreddit = entry["subreddit"]
    toxicity_class = entry["toxicity_class"]

    if subreddit not in toxicity_counts["normal"]:
        toxicity_counts["normal"][subreddit] = 0
    if subreddit not in toxicity_counts["flag"]:
        toxicity_counts["flag"][subreddit] = 0

    toxicity_counts[toxicity_class][subreddit] += 1

# Plotting
subreddits = list(toxicity_counts["normal"].keys())
bar_width = 0.35
index = np.arange(len(subreddits))

# Calculate percentages
total_counts = [toxicity_counts["normal"].get(subreddit, 0) + toxicity_counts["flag"].get(subreddit, 0) for subreddit in subreddits]
percentage_toxic = [toxicity_counts["flag"].get(subreddit, 0) / total_counts[i] * 100 if total_counts[i] != 0 else 0 for i, subreddit in enumerate(subreddits)]
percentage_normal = [toxicity_counts["normal"].get(subreddit, 0) / total_counts[i] * 100 if total_counts[i] != 0 else 0 for i, subreddit in enumerate(subreddits)]
# Plotting
bar_width = 0.35
index = np.arange(len(subreddits))

fig, ax = plt.subplots()
normal_bars = ax.bar(index, [toxicity_counts["normal"].get(subreddit, 0) for subreddit in subreddits], bar_width, label='Normal', color='blue')
toxic_bars = ax.bar(index + bar_width, [toxicity_counts["flag"].get(subreddit, 0) for subreddit in subreddits], bar_width, label='Toxic', color='red')

# Add percentage labels
for i, (toxic_bar, total_count) in enumerate(zip(toxic_bars, total_counts)):
    if total_count != 0:
        percentage_label = f"{percentage_toxic[i]:.2f}%"
        ax.text(toxic_bar.get_x() + toxic_bar.get_width() / 2, toxic_bar.get_height() + 1, percentage_label, ha='center', va='bottom')

# Add percentage labels
for i, (normal_bar, total_count) in enumerate(zip(normal_bars, total_counts)):
    if total_count != 0:
        percentage_label = f"{percentage_normal[i]:.2f}%"
        ax.text(normal_bar.get_x() + normal_bar.get_width() / 2, normal_bar.get_height() + 1, percentage_label, ha='center', va='bottom')


plt.xlabel('Subreddit')
plt.ylabel('Comments Count')
plt.title('Comments Count by Toxicity Class and Subreddit')
plt.xticks(index + bar_width / 2, subreddits, rotation=45, ha='right')
plt.legend()
plt.tight_layout()
#plt.show()

img1 = io.BytesIO()
plt.savefig(img1, format = 'png')
img1.seek(0)
politics_toxicity_data = urllib.parse.quote(base64.b64encode(img1.read()).decode())

data=None

plt.close()




# Access MongoDB collections
crime_collection = yt_crime_collection
politics_collection = yt_politics_collection

# Get distinct channel IDs
distinct_channel_ids = set(crime_collection.distinct("channel_id") + politics_collection.distinct("channel_id"))

# Initialize lists to store data for plotting
channel_names = []
crime_counts = []
politics_counts = []

# Fetch data for each channel ID
for channel_id in distinct_channel_ids:
    # Fetch the channel name for the current channel ID
    channel_document = crime_collection.find_one({"channel_id": channel_id}, {"channel_name": 1})
    channel_document2 = politics_collection.find_one({"channel_id": channel_id}, {"channel_name": 1})
    
    # Check if a document is found for the current channel ID
    if channel_document:
        channel_name = channel_document.get("channel_name", "Unknown")
    else:
        channel_name = channel_document2.get("channel_name", "Unknown")
    
    # Count the number of videos in crime collection for the current channel
    crime_count = crime_collection.count_documents({"channel_id": channel_id})
    
    # Count the number of videos in politics collection for the current channel
    politics_count = politics_collection.count_documents({"channel_id": channel_id})
    
    # Append data to lists
    channel_names.append(channel_name)
    crime_counts.append(crime_count)
    politics_counts.append(politics_count)

# Plotting
bar_width = 0.35
index = range(len(channel_names))

fig, ax = plt.subplots()
bar1 = ax.bar(index, crime_counts, bar_width, label='Crime', color='red')
bar2 = ax.bar([i + bar_width for i in index], politics_counts, bar_width, label='Politics', color='blue')

ax.set_xlabel('Channel Name')
ax.set_ylabel('Number of Videos')
ax.set_title('Number of Crime and Politics Videos for Each Channel')
ax.set_xticks([i + bar_width/2 for i in index])
ax.set_xticklabels(channel_names, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
img2 = io.BytesIO()
plt.savefig(img2, format='png')
img2.seek(0)
yt_per_channel_plot = urllib.parse.quote(base64.b64encode(img2.read()).decode())
#plt.show()
plt.close()



# Access MongoDB collections
crime_collection = yt_crime_collection
politics_collection = yt_politics_collection

# Count the number of videos in each collection
crime_count = crime_collection.count_documents({})
politics_count = politics_collection.count_documents({})

# Plotting
labels = ['Crime', 'Politics']
counts = [crime_count, politics_count]

plt.bar(labels, counts, color=['red', 'blue'])
plt.xlabel('Video Category')
plt.ylabel('Number of Videos')
plt.title('Number of Videos in Crime and Politics Collections')
# Save the plot as an image
img2 = io.BytesIO()
plt.savefig(img2, format='png')
img2.seek(0)
yt_category_plot = urllib.parse.quote(base64.b64encode(img2.read()).decode())
#plt.show()
plt.close()

# Fetch data from the collections
senti_data = comment_sentiment_collection.find({})
senti_youtube_data = yt_crime_sentiment_collection.find({})
#there

# Initialize counters for each sentiment range
sentiment_ranges = [f"{i/10:.2f}-{(i+1)/10:.2f}" for i in range(-10, 10)]
crime_counts = {range_: 0 for range_ in sentiment_ranges}
politics_counts = {range_: 0 for range_ in sentiment_ranges}
yt_crime_counts = {range_: 0 for range_ in sentiment_ranges}
yt_politics_counts = {range_: 0 for range_ in sentiment_ranges}

try:
    # Count comments in each sentiment range
    for entry in senti_data:
        # print(entry)
        sentiment_score = entry["sentiment_score"]
        collection_name = entry["collection_name"]

        # Increment the appropriate counter based on sentiment score
        for i in range(-10, 10):
            if i/10 <= sentiment_score < (i+1)/10:
                if collection_name == "Crime":
                    crime_counts[sentiment_ranges[i+10]] += 1
                elif collection_name == "Politics":
                    politics_counts[sentiment_ranges[i+10]] += 1
except Exception as e:
    logger.exception(f"couldn't find a field: {e}")

# Count YouTube comments in each sentiment range
for entry in senti_youtube_data:
    sentiment_score = entry["sentiment"]
    collection_name = entry["collection_name"]

    # Increment the appropriate counter based on sentiment score
    for i in range(-10, 10):
        if i/10 <= sentiment_score < (i+1)/10:
            if collection_name == "yt_crime":
                yt_crime_counts[sentiment_ranges[i+10]] += 1
            elif collection_name == "yt_politics":
                yt_politics_counts[sentiment_ranges[i+10]] += 1

# Convert counts to lists for plotting
sentiment_ranges_list = list(sentiment_ranges)
crime_counts_list = [crime_counts[range_] for range_ in sentiment_ranges]
politics_counts_list = [politics_counts[range_] for range_ in sentiment_ranges]
yt_crime_counts_list = [yt_crime_counts[range_] for range_ in sentiment_ranges]
yt_politics_counts_list = [yt_politics_counts[range_] for range_ in sentiment_ranges]

# Plot the data
bar_width = 0.2
index = np.arange(len(sentiment_ranges_list))

fig, ax = plt.subplots()
bar1 = ax.bar(index, crime_counts_list, bar_width, label='Crime')
bar2 = ax.bar(index + bar_width, politics_counts_list, bar_width, label='Politics')
bar3 = ax.bar(index + 2 * bar_width, yt_crime_counts_list, bar_width, label='yt_crime')
bar4 = ax.bar(index + 3 * bar_width, yt_politics_counts_list, bar_width, label='yt_politics')

ax.set_xlabel('Sentiment Score Ranges')
ax.set_ylabel('Number of Comments')
ax.set_title('Number of Comments in Each Sentiment Score Range')
ax.set_xticks(index + 2 * bar_width)
ax.set_xticklabels(sentiment_ranges_list,rotation=70)
ax.legend()

plt.tight_layout()

img2 = io.BytesIO()
plt.savefig(img2, format='png')
img2.seek(0)
sentimental_data = urllib.parse.quote(base64.b64encode(img2.read()).decode())
#plt.show()
plt.close()
