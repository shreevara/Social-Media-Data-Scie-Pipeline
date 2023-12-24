

README:

To run the crawler, we first install requirements specified in the requirments.txt by issuing the command: pip install -r requirements.txt

We need to have MongoDB installed as that is the database software we use for storing and retrieving the data.

After following the instructions for collecting data from our Project 2 implementation, we can view different plots for analysis by running the sm.py file. This starts a new Flask Server which gives a webpage with a dropdown list for the different analyses we have made.
We have added 2 plots with user input parameters under the names : Politics Toxicity Plot and Custom Sentimental Analysis Plot

Under the Politics Toxicity Plot, we can now input the subreddit by a drop-down list from which the toxicity results can be collected and displayed in real-time. This sends data stored in the database to ModerateHateSpeech API and plots the results. To add more subreddits in the dropdown list, we can specify that in the hatespeech_subreddits file line by line.
Example of plot with Ask_Politics subreddit data added:
![plot3](https://github.com/2023-Fall-CS-415-515/project-3-implementation-the-phoenix/assets/114188838/ebc96521-616c-4c44-946d-fc57b681f692)


In the Custom Sentimental Analysis Plot, we can input the range which we want to consider the threshold of negative, neutral and positive sentiments of the comments. For example, a user can specify any value less than -0.5 is considered as negative and anything greater than 0.5 is positive and the values in this range are neutral. This changes the plots as per the user's inputs useful for comparing sentiment analysis at different thresholds which was not visible in our previous plots.
Example of plot from thresholds -0.5 to 0.5
![plot1](https://github.com/2023-Fall-CS-415-515/project-3-implementation-the-phoenix/assets/114188838/82aabc50-1177-4a1d-bd2e-362a16560b4b)

Example of plot from thresholds -0.25 to 0.25
![plot2](https://github.com/2023-Fall-CS-415-515/project-3-implementation-the-phoenix/assets/114188838/4d3d2d4e-d079-4921-89fe-1dc8b23f986a)

