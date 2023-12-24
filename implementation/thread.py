from youtube import periodic_task
from reddit_analysis import collect_new_crime_data, collect_new_political_data
import threading
import time
from log_config import setup_logging
logger = setup_logging()

# Define the interval for running the periodic task (e.g., 1 hour)
interval_youtube_hours = 6
interval_reddit_mins=5
def threaded_periodic_task():
    while True:
        try:
            periodic_task()
        except Exception as e:
            logger.exception(f"Exception occured while running periodic task for yt collection: {e}")
        logger.info("Succesfully completed the job for yt collection")
        time.sleep(interval_youtube_hours * 3600)  # Sleep for the specified interval

def threaded_reddit_task():
    while True:
        try:
            collect_new_crime_data()
            collect_new_political_data()
        except Exception as e:
            logger.exception(f"Exception occured while running task for reddit collection: {e}")
        logger.info("Succesfully completed the job for reddit data collection")
        time.sleep(interval_reddit_mins * 60)  # Sleep for the specified interval

# Start the threaded periodic task
try:
    ythread = threading.Thread(target=threaded_periodic_task)
    rthread = threading.Thread(target=threaded_reddit_task)
    ythread.daemon = True  # The thread will exit when the main program exits
    rthread.daemon = True 
    ythread.start()
    rthread.start()
except Exception as e:
    logger.exception(f"Exception occured while running threads: {e}")

# Keep the main program running (indefinitely) to allow the periodic task to continue
while True:
    pass