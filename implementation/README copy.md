[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/T3nUFdmQ)

README:

To run the crawler, we first install requirements specified in the requirments.txt by issuing the command:
pip install -r requirements.txt

We need to have MongoDB installed as that is the database software we use for storing and retrieving the data.

Then to run the main crawler of our project for collecting Youtube and Reddit data, we run the thread.py file by:
python3 thread.py

This program is designed to collect data from Reddit every 5 minutes and from Youtube every 6 hours due to the API limitations and can run as long as the system is active.

After collecting a sizeable data for analysis, we can then run a program for classifying Youtube videos whether they talk about Politics or Crime by running topic_classifer.py by:
python3 topic_classifier.py

After the classifier finishes classifying data from Youtube, we can now plot the data using the sm.py file which runs a Flask server on the machine by typing:
python3 sm.py

In this simple webpage, we can choose the plots by the dropdown list and view the plots we have developed.

We have used comments data from the r/democrats and r/Republicans subreddit to evaluate toxicity by using the ModerateHateSpeech API. After running our thread.py for sometime, we can run the HateSpeech_collection.py to collect Toxicity results from subreddits defined in the hatespeech_subreddits file line by line.
Then after collecting enough data, we can view the a plot in the sm.py file where we have plotted a graph of subreddits and the count of normal/toxic comments.

We have also developed a program to analyze the general sentiments of the comments for both Reddit and Youtube datasets. To do that, we run the Sentiment_Analysis_reddit.py file for sometime which classifies the comments in the score range of -1.0 to 1.0 where scores near or -1.0 is termed as negative and scores near or equal to 0 is neutral and near 1.0 means more positive. This data is stored in the database in a seperate collection.
To view a graph of the overall sentiments of comments, we can run the sm.py file to see the plot in the dropdown list.

Politics Comments crawler:

To collect the new comments of r/politics subreddit posted,we run the reddit_comments.py which collects the data from Reddit API every 4 minutes and we can view the plot from the sm.py file which runs the webserver


