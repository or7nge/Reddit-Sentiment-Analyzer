import praw
import os
from textblob import TextBlob
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id="UxOkdinyS1FyBxE51Urmfg",
    client_secret="TzKYf8WOfLEHNPDRZMU2uYaz3yfxEg",
    user_agent="python:my_sentiment_analyzer:1.0 (by /u/Good_Explorer_8970)"
)

app = Flask(__name__, static_folder='templates')


def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"


def parse_reddit(subreddit_name, keyword):
    subreddit = reddit.subreddit(subreddit_name)
    results = []
    for post in subreddit.search(keyword, limit=100):
        sentiment = analyze_sentiment(post.title + " " + post.selftext)
        results.append({
            "title": post.title,
            "content": post.selftext[:200] + "..." if len(post.selftext) > 200 else post.selftext,
            "sentiment": sentiment
        })
    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subreddit = request.form['subreddit']
        keyword = request.form['keyword']
        results = parse_reddit(subreddit, keyword)
        return render_template('results.html', results=results)
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.json
    subreddit = data.get('subreddit')
    keyword = data.get('keyword')
    if not subreddit or not keyword:
        return jsonify({"error": "Missing subreddit or keyword"}), 400
    results = parse_reddit(subreddit, keyword)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
