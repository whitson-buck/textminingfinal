import pandas as pd
import os

# List of file names
file_names = [
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

# Read each CSV file into a DataFrame and append to a list
dfs = []
for file_name in file_names:
    df = pd.read_csv(file_name)
    dfs.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

# Add columns for Review_name, Review_content, Date_of_review, and Type_of_wine
combined_df['Review_name'] = combined_df['Unnamed: 0']
combined_df['Review_content'] = combined_df['Unnamed: 1']
combined_df['Date_of_review'] = combined_df['Unnamed: 2']
combined_df['Type_of_wine'] = combined_df['Unnamed: 3']

# Drop unnecessary columns
combined_df.drop(columns=['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'], inplace=True)

# Display the combined DataFrame
print(combined_df)
