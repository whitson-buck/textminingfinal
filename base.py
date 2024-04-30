import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process

# List of file names for the wine reviews dataset
review_file_names = [
    'Wine_Reviews_2022_12_10.csv',
    'Wine_Reviews_2023_01_16.csv',
    'Wine_Reviews_2023_03_09.csv',
    'Wine_Reviews_2023_06_17.csv',
    'Wine_Reviews_2023_09_07.csv',
    'Wine_Reviews_2023_10_05.csv',
    'Wine_Reviews_2023_11_08.csv',
    'Wine_Reviews_2023_12_17.csv',
    'Wine_Reviews_2024_01_14.csv',
    'Wine_Reviews_2024_02_11.csv',
    'Wine_Reviews_2024_03_11.csv',
    'Wine_Reviews_2024_04_15.csv'
]

# Read each wine review CSV file into a DataFrame and append to a list
review_dfs = []
for file_name in review_file_names:
    df = pd.read_csv(file_name)
    review_dfs.append(df)

# Concatenate all wine review DataFrames into one
combined_review_df = pd.concat(review_dfs, ignore_index=True)

# Load the second dataset
second_df = pd.read_csv('winemag-data-130k-v2.csv')

# Extract wine names from both datasets
wine_names_review = combined_review_df['Review_name'].unique()
wine_names_second = second_df['title'].unique()

# Calculate TF-IDF vectors for wine names
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(list(wine_names_review) + list(wine_names_second))

# Calculate cosine similarity between TF-IDF vectors
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Match wine names based on closest cosine similarity
matches = {}
for i, wine_name in enumerate(wine_names_review):
    # Find the index of the most similar wine name from the second dataset
    most_similar_index = cosine_sim[i].argsort()[-1]
    # Store the matched wine name and its similarity score
    matches[wine_name] = (wine_names_second[most_similar_index], cosine_sim[i][most_similar_index])

# Create a DataFrame to store the matched wine names and similarity scores
matches_df = pd.DataFrame.from_dict(matches, orient='index', columns=['Matched_wine_name', 'Cosine_similarity'])

# Reset the index of the DataFrame
matches_df.reset_index(inplace=True)
matches_df.rename(columns={'index': 'Review_name'}, inplace=True)

# Display the DataFrame with matched wine names
print(matches_df)
