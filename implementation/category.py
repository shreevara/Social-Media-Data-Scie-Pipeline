import pymongo
from datetime import datetime
import matplotlib.pyplot as plt3
from collections import defaultdict
import io, urllib, base64
from db import youtube_collection
from authentication import headers
from log_config import setup_logging
logger = setup_logging()

# Access the YouTube collection
#youtube_collection = mongo["Crawler"]["Newsinfo"]

# Query the collection and process the data
try:
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
except Exception as e:
    logger.exception(f"an exception occured: {e}")

# Create lists for plotting
dates_plot = list(comment_counts_by_date.keys())
comment_counts = list(comment_counts_by_date.values())

# Plot the line graph
plt3.plot(dates_plot, comment_counts, marker='o')
plt3.xlabel('Date')
plt3.ylabel('Number of Comments')
plt3.title('Number of Comments for Each Video on a Given Day')
plt3.xticks(rotation=45)
plt3.tight_layout()

img3 = io.BytesIO()
plt3.savefig(img3, format = 'png')
img3.seek(0)
yt_comments_data = urllib.parse.quote(base64.b64encode(img3.read()).decode())


plt3.show(block=True)
