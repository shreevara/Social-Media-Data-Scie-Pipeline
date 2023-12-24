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
from datetime import datetime, timezone, timedelta
import time
import threading
from collections import Counter
import matplotlib.pyplot as plt
df = pd.DataFrame()
from log_config import setup_logging
logger = setup_logging()

target_date = "2023-11-27"
#cursor = politics_comments_collection.find()
cursor = politics_comments_collection.find({"postedtime(est)": {"$gte": datetime.fromisoformat(target_date), "$lt": datetime.fromisoformat(target_date) + timedelta(days=1) }})
# Initialize a Counter to count comments for each minute
comments_counter = Counter()

# Iterate through the documents and count comments per minute
try:
    for document in cursor:
        posted_time = document.get("postedtime(est)", {}).strftime("%Y-%m-%d %H:%M")
        
        if posted_time:
            # Convert posted_time to a Python datetime object
            posted_time = datetime.fromisoformat(posted_time)
            # Extract minute-level information (you can also include seconds for more precision)
            hour = posted_time.strftime("%H")+":00"
            comments_counter[hour] += 1
except Exception as e:
    logger.exception("error occured!: {e}")

# Separate the data into x (timestamps) and y (comment counts)
x = list(comments_counter.keys())
y = list(comments_counter.values())

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(x, y, marker='o')
plt.xticks(rotation=45)
plt.xlabel("Date and Time")
plt.ylabel("Comment Count")
plt.title("Number of Comments Per Hour On "+target_date)
plt.tight_layout()

# Show the plot
plt.show()