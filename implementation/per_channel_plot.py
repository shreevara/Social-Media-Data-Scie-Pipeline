import pymongo
import matplotlib.pyplot as plt
from db import yt_crime_collection, yt_politics_collection, youtube_collection
import io, urllib, base64
from log_config import setup_logging
logger = setup_logging()

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
try:
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
except Exception as e:
    logger.exception(f"error occured!: {e}")

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
yt_classfied_plot2 = urllib.parse.quote(base64.b64encode(img2.read()).decode())
#plt.show()
plt.close()
