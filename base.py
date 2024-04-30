import pandas as pd
from fuzzywuzzy import process
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, request, render_template_string

# Read expert and amateur data
expert_data = pd.read_csv("winemag-data-130k-v2.csv")
amateur_files = [
    "Wine_Reviews_2022_12_10.csv",
    "Wine_Reviews_2023_01_16.csv",
    "Wine_Reviews_2023_03_09.csv",
    "Wine_Reviews_2023_06_17.csv",
    "Wine_Reviews_2023_09_07.csv",
    "Wine_Reviews_2023_10_05.csv",
    "Wine_Reviews_2023_11_08.csv",
    "Wine_Reviews_2023_12_17.csv",
    "Wine_Reviews_2024_01_14.csv",
    "Wine_Reviews_2024_02_11.csv",
    "Wine_Reviews_2024_03_11.csv",
    "Wine_Reviews_2024_04_15.csv"
]
amateur_data = pd.concat([pd.read_csv(file) for file in amateur_files])

# Merge amateur data into a single DataFrame
amateur_data['Type_of_wine'] = amateur_data['Type_of_wine'].str.lower()
amateur_data = amateur_data.groupby(['Type_of_wine']).agg({'Review_name': ' '.join, 'Review_content': ' '.join}).reset_index()

# Fuzzy matching to link expert and amateur data
def fuzzy_merge(df1, df2, key1, key2, threshold=90, limit=1):
    df1[key1] = df1[key1].astype(str)
    df2[key2] = df2[key2].astype(str)
    matches = df1[key1].apply(lambda x: process.extract(x, df2[key2], limit=limit))
    df1['matches'] = matches
    df1['matches'] = df1['matches'].apply(lambda x: x[0] if len(x) > 0 else None)
    return df1

expert_data['matches'] = None
merged_data = fuzzy_merge(expert_data, amateur_data, 'title', 'Type_of_wine')

# Sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_textblob = blob.sentiment.polarity
    analyzer = SentimentIntensityAnalyzer()
    sentiment_vader = analyzer.polarity_scores(text)['compound']
    return sentiment_textblob, sentiment_vader

merged_data['sentiment_textblob'], merged_data['sentiment_vader'] = zip(*merged_data['Review_content'].apply(analyze_sentiment))

# Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_wine = request.form['wine']
        wine_data = merged_data[merged_data['title'] == selected_wine]
        return render_template_string('''<h2>{{ title }}</h2>
                                        <p><strong>Sentiment (TextBlob):</strong> {{ sentiment_textblob }}</p>
                                        <p><strong>Sentiment (VADER):</strong> {{ sentiment_vader }}</p>''',
                                        title=selected_wine,
                                        sentiment_textblob=wine_data['sentiment_textblob'].iloc[0],
                                        sentiment_vader=wine_data['sentiment_vader'].iloc[0])
    else:
        wines = merged_data['title'].unique().tolist()
        return render_template_string('''<form method="post">
                                        <select name="wine">
                                        {% for wine in wines %}
                                        <option value="{{ wine }}">{{ wine }}</option>
                                        {% endfor %}
                                        </select>
                                        <input type="submit" value="Submit">
                                        </form>''', wines=wines)

if __name__ == '__main__':
    app.run(debug=True)

