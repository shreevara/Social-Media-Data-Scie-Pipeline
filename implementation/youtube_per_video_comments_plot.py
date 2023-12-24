import pymongo
from datetime import datetime
import matplotlib.pyplot as plt2
import io, urllib, base64
from db import youtube_collection
from authentication import headers
from log_config import setup_logging
logger = setup_logging()


# Access the YouTube collection
# youtube_collection = mongo["Crawler"]["Newsinfo"]

# Query the collection and process the data
yt_data = youtube_collection.find({})
comment_data = []
max_comments_per_day = {}

try:
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
except Exception as e:
    logger.exception(f"an exception occured!: {e}")

# Create lists for plotting
dates = [item["date"] for item in comment_data]
comment_counts = [item["comment_count"] for item in comment_data]

# Plot the line graph
plt2.plot(dates, comment_counts, marker='o', linestyle='None')
plt2.xlabel('Date')
plt2.ylabel('Number of Comments')
plt2.title('Number of Comments for Each Video on a Given Day')
plt2.xticks(rotation=45)
plt2.tight_layout()

# Save the plot as an image
img2 = io.BytesIO()
plt2.savefig(img2, format='png')
img2.seek(0)
yt_comments_data = urllib.parse.quote(base64.b64encode(img2.read()).decode())

# Show the plot
plt2.show()

# Print information about the video with the highest comments for each day
print("Maximum Comments for Each Day:")
for date, info in max_comments_per_day.items():
    print("***********************************\n")
    print(f"Date: {date}")
    print("Video ID:", info["video_id"])
    print("Title:", info["title"])
    #print("Description:", info["description"])
    print("Number of Comments:", info["comments"])
    print("-" * 30)
