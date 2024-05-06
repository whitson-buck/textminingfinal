import csv
from flask import Flask, render_template, request
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from afinn import Afinn
import nltk
import pandas as pd
nltk.download('vader_lexicon')

app = Flask(__name__)

# Initialize the sentiment analyzers
sid = SentimentIntensityAnalyzer()
afinn = Afinn()

# Read data from CSV file
data = pd.read_csv("merged_data.csv")

# Debug print to check if data is loaded
print(data.head())

# Route for home page
@app.route('/')
def home():
    wine_categories = data['expert_variety'].unique().tolist() # Accessing the 'expert_variety' column
    return render_template('index.html', wine_categories= wine_categories)

# Route for analyzing sentiments
@app.route('/analyze', methods=['POST'])
def analyze():
    # Get selected wine category from the form data
    selected_category = request.form['category']
    
    # Filter data for selected category
    selected_data = data[data['expert_variety'] == selected_category]
    
    if selected_data.empty:
        return "No reviews found for the selected category", 404

    # Perform sentiment analysis on both amateur and expert reviews
    amateur_reviews = selected_data.dropna(subset=['reviews.text'])
    expert_reviews = selected_data.dropna(subset=['expert_description'])

    amateur_textblob_sentiments = [TextBlob(review).sentiment for review in amateur_reviews['reviews.text']]
    amateur_vader_sentiments = [sid.polarity_scores(review) for review in amateur_reviews['reviews.text']]
    amateur_afinn_sentiments = [afinn.score(review) for review in amateur_reviews['reviews.text']]

    expert_textblob_sentiments = [TextBlob(description).sentiment for description in expert_reviews['expert_description']]
    expert_vader_sentiments = [sid.polarity_scores(description) for description in expert_reviews['expert_description']]
    expert_afinn_sentiments = [afinn.score(description) for description in expert_reviews['expert_description']]

    return render_template('result.html', selected_category=selected_category,
                           amateur_reviews=amateur_reviews, expert_reviews=expert_reviews,
                           amateur_textblob_sentiments=amateur_textblob_sentiments,
                           amateur_vader_sentiments=amateur_vader_sentiments,
                           amateur_afinn_sentiments=amateur_afinn_sentiments,
                           expert_textblob_sentiments=expert_textblob_sentiments,
                           expert_vader_sentiments=expert_vader_sentiments,
                           expert_afinn_sentiments=expert_afinn_sentiments)
if __name__ == '__main__':
    app.run(debug=True)
