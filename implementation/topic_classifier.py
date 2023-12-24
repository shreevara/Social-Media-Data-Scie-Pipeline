from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn import metrics
from db import crime_collection, politics_collection, youtube_collection, yt_crime_collection, yt_politics_collection
import nltk
from nltk.corpus import stopwords
from log_config import setup_logging
logger = setup_logging()

nltk.download("vader_lexicon", quiet=True)
nltk.download("stopwords")

posts_crime = crime_collection.find()
l = []
for i in posts_crime:
    l.append(i["title"]+" "+i["selftext"])
print(len(l))

posts_crime = politics_collection.find()
ll = []
for i in posts_crime:
    ll.append(i["title"]+" "+i["selftext"])
print(len(ll))

video = youtube_collection.find_one({"channel_id" : "UCupvZG-5ko_eiXAupbDfxWw"})
print(video["top_videos"][1]["title"])

crime_text = video["top_videos"][1]["top_comments"]
politics_text = video["top_videos"][2]["top_comments"]

crime_text+= l

politics_text+= ll

print(crime_text)

total_text = [*crime_text, *politics_text]
crime_category = ["Crime"]*len(crime_text)
politics_category = ["Politics"]*len(politics_text)

total_category = [*crime_category, *politics_category]

data = {
    "text" : total_text,
    "category" : total_category
}

print(data)


import pandas as pd
df = pd.DataFrame(data)

def cleaning(dataframe):
    dataframe["Cleaned Text"] = (
        dataframe["text"]
        .str.strip()
        .str.replace("\n", " ")
        .str.replace(r"(?:\@|http?\://|https?\://|www)\S+", "", regex=True)
        .str.replace(r"[^\w\s]+", "", regex=True)
        .str.lower()
        .str.replace(r"\d+", "", regex=True)
        .str.replace(r"#\S+", " ", regex=True)
    )

    stop_words = stopwords.words("english")
    dataframe["Cleaned Text"] = dataframe["Cleaned Text"].apply(
        lambda comment: " ".join([word for word in comment.split() if word not in stop_words])
    )
  
    return dataframe

df = cleaning(df)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['Cleaned Text'], df['category'], random_state=42)

# Create a pipeline with a CountVectorizer and a Naive Bayes classifier
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)


# Iterate through all documents in youtube_collection
for entry in youtube_collection.find():
    for video in entry["top_videos"]:
        # Extract relevant information
        channel_name = entry["channel_name"]
        channel_id = entry["channel_id"]
        video_id = video["video_id"]
        title = video["title"]
        description = video["description"]
        date = video["date"]
        view_count = video["view_count"]
        top_comments = video["top_comments"]

        # Combine title and description for classification
        text = f"{title} {description}"

        # Clean the text
        cleaned_text = cleaning(pd.DataFrame({"text": [text]}))["Cleaned Text"][0]

        # Predict the category
        prediction = model.predict([cleaned_text])[0]

        # Prepare the document for insertion
        doc = {
            "channel_name": channel_name,
            "channel_id": channel_id,
            "top_videos": [
                {
                    "video_id": video_id,
                    "title": title,
                    "description": description,
                    "date": date,
                    "view_count": view_count,
                    "top_comments": top_comments
                }
            ]
        }

        # Add the document to the appropriate collection
        if prediction == "Crime":
            yt_crime_collection.insert_one(doc)
        elif prediction == "Politics":
            yt_politics_collection.insert_one(doc)