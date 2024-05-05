import csv
from flask import Flask, render_template, request
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from afinn import Afinn
import nltk
nltk.download('vader_lexicon')

app = Flask(__name__)

# Initialize the sentiment analyzers
sid = SentimentIntensityAnalyzer()
afinn = Afinn()

# Read data from CSV file
data = []
with open('merged_data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# Debug print to check if data is loaded
print(data)

# Route for home page
@app.route('/')
def home():
    categories = set(d['expert_variety'] for d in data)
    return render_template('index.html', categories=categories)

# Route for analyzing sentiments
@app.route('/analyze', methods=['POST'])
def analyze():
    category = request.form['category']
    selected_data = [d for d in data if d['expert_variety'] == category]

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
