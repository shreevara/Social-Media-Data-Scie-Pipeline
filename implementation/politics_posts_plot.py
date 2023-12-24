# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 14:59:01 2023

@author: haris
"""

import pandas as pd
# from hello import res
import json
import requests
from db import crime_collection, politics_collection, politics_comments_collection
from authentication import headers
import pytz
import base64
import urllib
import io
from datetime import datetime, timezone, timedelta
import time
import threading
from collections import Counter
import matplotlib.pyplot as plt1
df = pd.DataFrame()
from log_config import setup_logging
logger = setup_logging()

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
plt1.figure(figsize=(12, 6))
plt1.bar(x, y, color='skyblue')
plt1.xticks(rotation=45)
plt1.xlabel("Date")
plt1.ylabel("Comment Count")
plt1.title("Number of Posts Per Day (Nov 1, 2023 - Nov 14, 2023)")
plt1.tight_layout()

img1 = io.BytesIO()
plt1.savefig(img1, format = 'png')
img1.seek(0)
politics_posts_data = urllib.parse.quote(base64.b64encode(img1.read()).decode())
# return render_template('flask_form_plot.html', plot_url = plot_data)
# render_template('flask_form_plot.html', plot_url = plot_data)

# Show the plot
# plt1.show(block=True)