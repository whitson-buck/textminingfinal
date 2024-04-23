from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

app = Flask(__name__)

# Function to scrape IMDb for top movies
def scrape_imdb_top_movies():
    url = "https://www.imdb.com/chart/top/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []
    for movie in soup.select('.titleColumn a'):
        movies.append(movie.text)
    return movies[:100]

# Function to scrape Metacritic for reviews
def scrape_metacritic_reviews(movie):
    url = f"https://www.metacritic.com/movie/{movie.replace(' ', '-')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = []
    for review in soup.select('.metascore_w'):
        reviews.append(int(review.text))
    return reviews[:5]

# Function to perform sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

@app.route('/')
def index():
    top_movies = scrape_imdb_top_movies()
    return render_template('index.html', movies=top_movies)

@app.route('/movie/<movie>')
def movie_details(movie):
    metacritic_reviews = scrape_metacritic_reviews(movie)
    imdb_reviews = []  # Placeholder for IMDb reviews (You need to implement this)
    metacritic_sentiments = [analyze_sentiment(review) for review in metacritic_reviews]
    imdb_sentiments = []  # Placeholder for IMDb sentiment analysis results
    return render_template('movie_details.html', movie=movie, metacritic_reviews=metacritic_reviews,
                           imdb_reviews=imdb_reviews, metacritic_sentiments=metacritic_sentiments,
                           imdb_sentiments=imdb_sentiments)

if __name__ == '__main__':
    app.run(debug=True)
