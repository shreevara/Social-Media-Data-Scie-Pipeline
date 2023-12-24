# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 14:59:01 2023

@author: haris
"""

import pandas as pd
# from hello import res
import json
import requests
from db import politics_comments_collection
from authentication import headers
#import pytz
import io, urllib, base64
from datetime import datetime, timezone, timedelta
import time
import threading
from collections import Counter
import matplotlib.pyplot as plt2
from matplotlib.dates import HourLocator
from log_config import setup_logging
logger = setup_logging()

# Query data from MongoDB
data = list(politics_comments_collection.find({"postedtime(est)": {"$gte": datetime.fromisoformat("2023-11-01"), "$lt": datetime.fromisoformat("2023-11-29") }}))

# Convert data to DataFrame
df = pd.DataFrame(data)

# Convert "postedtime(est)" to datetime format
df["postedtime(est)"] = pd.to_datetime(df["postedtime(est)"])

# Set the date range (1st November to 14th November)
start_date = datetime(2023, 11, 1)
end_date = datetime(2023, 11, 29, 23, 59, 59)

# Create bins hourly
date_bins = pd.date_range(start=start_date, end=end_date, freq='H')

# Plot the graph
plt2.figure(figsize=(30, 12))
plt2.hist(df["postedtime(est)"], bins=date_bins, edgecolor='black', alpha=0.7)
plt2.title('Number of Posts per Hour')
plt2.xlabel('Date and Hour')
plt2.ylabel('Number of Posts')
plt2.xticks(rotation=45)
plt2.tight_layout()

img2 = io.BytesIO()
plt2.savefig(img2, format = 'png')
img2.seek(0)
pol_comments_data = urllib.parse.quote(base64.b64encode(img2.read()).decode())


plt2.show()