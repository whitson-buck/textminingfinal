from flask import Flask, render_template, request
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from afinn import Afinn

app = Flask(__name__)

# Initialize the sentiment analyzers
sid = SentimentIntensityAnalyzer()
afinn = Afinn()

# Sample dataset
data = 

# Route for home page
@app.route('/')
def home():
    return render_template('index.html', data=data)

# Route for analyzing sentiments
@app.route('/analyze', methods=['POST'])
def analyze():
    category = request.form['category']
    selected_data = [d for d in data if d['name'] == category]

    if not selected_data:
        return "Category not found", 404

    # Sentiment analysis using TextBlob
    textblob_sentiments = [TextBlob(d['reviews.text']).sentiment for d in selected_data]

    # Sentiment analysis using VADER
    vader_sentiments = [sid.polarity_scores(d['reviews.text']) for d in selected_data]

    # Sentiment analysis using AFINN
    afinn_sentiments = [afinn.score(d['reviews.text']) for d in selected_data]

    return render_template('result.html', category=category, selected_data=selected_data, 
                           textblob_sentiments=textblob_sentiments, vader_sentiments=vader_sentiments,
                           afinn_sentiments=afinn_sentiments)

if __name__ == '__main__':
    app.run(debug=True)
