import csv
from flask import Flask, render_template, request
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from afinn import Afinn
import nltk
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

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
    expert_reviews = selected_data.dropna(subset=['expert_description']).head(1)

    amateur_textblob_sentiments = [TextBlob(review).sentiment for review in amateur_reviews['reviews.text']]
    amateur_vader_sentiments = [sid.polarity_scores(review)['compound'] for review in amateur_reviews['reviews.text']]
    amateur_afinn_sentiments = [afinn.score(review) for review in amateur_reviews['reviews.text']]

    expert_textblob_sentiments = [TextBlob(description).sentiment for description in expert_reviews['expert_description']]
    expert_vader_sentiments = [sid.polarity_scores(description)['compound'] for description in expert_reviews['expert_description']]
    expert_afinn_sentiments = [afinn.score(description) for description in expert_reviews['expert_description']]

    # Calculate average sentiment scores
    amateur_average = sum(amateur_vader_sentiments) / len(amateur_vader_sentiments) if amateur_vader_sentiments else 0
    expert_average = sum(expert_vader_sentiments) / len(expert_vader_sentiments) if expert_vader_sentiments else 0

    # Calculate difference between average sentiment scores
    difference = amateur_average - expert_average

    result = "Amateurs enjoy more" if difference > 0 else "Experts enjoy more" if difference < 0 else "Both enjoy equally"

    return render_template('result.html', selected_category=selected_category,
                           amateur_reviews=amateur_reviews, expert_reviews=expert_reviews,
                           amateur_textblob_sentiments=amateur_textblob_sentiments,
                           amateur_vader_sentiments=amateur_vader_sentiments,
                           amateur_afinn_sentiments=amateur_afinn_sentiments,
                           expert_textblob_sentiments=expert_textblob_sentiments,
                           expert_vader_sentiments=expert_vader_sentiments,
                           expert_afinn_sentiments=expert_afinn_sentiments, result=result,
                           difference=difference)


@app.route('/top_words')
def top_words():
    # Tokenize and remove stop words
    stop_words = set(stopwords.words('english'))

    expert_words = []
    amateur_words = []

    for expert_review in data['expert_description'].dropna():
        words = nltk.word_tokenize(expert_review.lower())
        expert_words.extend([word for word in words if word.isalpha() and word not in stop_words])

    for amateur_review in data['reviews.text'].dropna():
        words = nltk.word_tokenize(amateur_review.lower())
        amateur_words.extend([word for word in words if word.isalpha() and word not in stop_words])

    # Count occurrences of words
    expert_word_counts = Counter(expert_words)
    amateur_word_counts = Counter(amateur_words)

    # Get top ten words for experts and amateurs
    top_ten_expert_words = expert_word_counts.most_common(10)
    top_ten_amateur_words = amateur_word_counts.most_common(10)

    total_words_expert = sum(len(text.split()) for text in expert_word_counts)
    total_words_amateur = sum(len(text.split()) for text in amateur_word_counts)

    expert_review_count = len(set(data['expert_description'].dropna()))
    amateur_review_count = len(set(data['reviews.text'].dropna()))

    wpr_expert = round(total_words_expert / expert_review_count,2) if expert_review_count > 0 else 0

    wpr_amateur = round(total_words_amateur / amateur_review_count,2) if amateur_review_count > 0 else 0

    # Get top ten words for experts and amateurs
    top_ten_expert_words = expert_word_counts.most_common(10)
    top_ten_amateur_words = amateur_word_counts.most_common(10)

    sid = SentimentIntensityAnalyzer()
    expert_sentiments = sid.polarity_scores(' '.join(data['expert_description'].dropna()))
    amateur_sentiments = sid.polarity_scores(' '.join(data['reviews.text'].dropna()))

    return render_template('top_words.html', 
                           top_ten_expert=top_ten_expert_words,
                           top_ten_amateur=top_ten_amateur_words,
                           total_words_expert=total_words_expert,
                           total_words_amateur=total_words_amateur,
                           expert_review_count=expert_review_count,
                           amateur_review_count=amateur_review_count,
                           expert_sentiments=expert_sentiments,
                           amateur_sentiments=amateur_sentiments,
                           wpr_expert=wpr_expert,
                           wpr_amateur=wpr_amateur)
if __name__ == '__main__':
    app.run(debug=True)


