from flask import Flask, Response, render_template, request, redirect, url_for, session
import pymongo
import json
import io
#from reddit_analysis import collect_new_crime_data, collect_new_political_data
#from db import crime_collection, politics_collection
import time
import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from all_plots import politics_posts_data,pol_comments_data, yt_comments_data, politics_toxicity_data, yt_per_video_comments_data, yt_per_channel_plot, yt_category_plot, sentimental_data
#from init_db import update_crime_subreddit, update_political_subreddit, insert_channel_ids
from Sentimental_Custom_Plot import sentimental_plot
from HateSpeech import HateSpeech_insert
app = Flask(__name__)
app.secret_key = 'sm'

##################################
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {"fname" : "murali", "lname":"ponnada"}
        dbresponse = db.users.insert_one(user)
        print(dbresponse.inserted_id)
        return Response(
            response=json.dumps(
                {
                    "message":"user_created",
                    "id":f"{dbresponse.inserted_id} {user['fname']}"
                }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)

@app.route("/", methods=["GET"])
def get_user():
    return render_template('home.html')

# @app.route("/politics_posts_plot", methods=["GET"])
# def get_politics_posts_plot():
#     return render_template('politics_posts_plot.html', plot_url = politics_posts_data)

# @app.route("/pol_comments_plot", methods=["GET"])
# def get_pol_comments_plot():
#     return render_template('pol_comments_plot.html', plot_url = pol_comments_data)

# @app.route("/youtube_plot", methods=["GET"])
# def get_all_plots():
#     return render_template('all_plots.html', plot_url1 = politics_posts_data, plot_url2 = pol_comments_data)

@app.route("/redirect",methods=['GET', 'POST'])
def options():
    option = request.args.get("options")
    if option == "politics_posts_plot": 
      return render_template('politics_posts_plot.html', plot_url1 = politics_posts_data)

    elif option == "pol_comments_plot":
      return render_template('pol_comments_plot.html', plot_url2 = pol_comments_data)

    elif option == "youtube_plot":
      return render_template('youtube_plot.html',plot_url3=yt_comments_data)

    elif option =="politics_toxicity_plot":
        
        
        try:
            with open('hatespeech_subreddits', 'r') as file:
                # Read the lines from the file and remove newline characters
                
                subreddits = [line.strip() for line in file]
                print(subreddits)
        except Exception as e:
            #logger.exception(f"exception occured while reading the file `hatespeech_subreddits`: {e}")
            print(e)
        return render_template('politics_toxicity_plot.html',plot_url4=politics_toxicity_data, subreddit_option=subreddits)

    elif option =="youtube_per_video_plot":
      return render_template('youtube_per_video_plot.html',plot_url5=yt_per_video_comments_data)

    elif option =="youtube_per_channel_plot":
      return render_template('youtube_per_channel_plot.html',plot_url6=yt_per_channel_plot)

    elif option =="youtube_category_plot":
      return render_template('youtube_category_plot.html',plot_url7=yt_category_plot)

    elif option =="sentimental_plot":
        
        return render_template('sentimental_plot.html',plot_url8=sentimental_data)
    
    elif option =="sentimental_custom_plot":
        
        return redirect(url_for('inputsenti'))

@app.route("/select_subreddit", methods=['POST'])
def select_subreddit():
    if request.method == 'POST':
        selected_subreddit = request.form.get('dropdown')
        session['selected_subreddit'] = selected_subreddit
        
    selected_subreddit=session.get('selected_subreddit')
    #if not selected_subreddit:
        #return redirect(url_for('options'))
    HateSpeech_insert(selected_subreddit)
    return redirect(url_for('options'))

@app.route("/inputsenti", methods=['GET','POST'])
def inputsenti():
    if request.method == 'POST':
        min_senti_score = float(request.form.get('min_senti_score'))
        max_senti_score = float(request.form.get('max_senti_score'))
        print(min_senti_score, max_senti_score)
        sentimental_data = sentimental_plot(min_senti_score, max_senti_score)
        return render_template('sentimental_custom_plot.html',plot_url9=sentimental_data)
    return render_template('sentimental_custom_plot.html')

'''@app.route("/subreddits", methods=[""])
def subreddits():
    option = request.args.get("options")
    subreddit = request.form["text"]
    res = "NoAction"
    if option == "crime":
        res = update_crime_subreddit(subreddit)
    elif option == "politics":
        res = update_political_subreddit(subreddit)
    return Response(
            response=json.dumps(
                {
                    "message":res,
                }),
            status=200,
            mimetype="application/json"
        )


@app.route("/pnewcrime", methods=["GET"])
def get_crime_data():
    try:
        # crime_records = collect_new_crime_data()
        # dbresponse = crime_collection.insert_many(crime_records)
        print("-------------------INSIDE PNEWCRIME--------------------")
        # print(crime_records)
        return Response(
            response=json.dumps(
                {
                    "message":"crime_reddit_data_created"
                }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("----------------------------"+str(ex)+"---------------------------"+str(datetime.datetime.now()))

@app.route("/pnewpolitics", methods=["GET"])
def get_data():
    try:
        # political_records = collect_new_political_data()
        # dbresponse = politics_collection.insert_many(records)
        print("-------------------INSIDE PNEWPOLITICS--------------------")
        return Response(
            response=json.dumps(
                {
                    "message":"political_reddit_data_created"
                }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
##################################
'''
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)