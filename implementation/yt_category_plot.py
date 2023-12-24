import pymongo
import matplotlib.pyplot as plt
from db import yt_crime_collection, yt_politics_collection
import io, urllib, base64
from log_config import setup_logging
logger = setup_logging()

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
yt_classfied_plot = urllib.parse.quote(base64.b64encode(img2.read()).decode())
#plt.show()
plt.close()
