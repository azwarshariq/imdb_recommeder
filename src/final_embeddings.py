import os

directory = 'data'  # Path to the directory

file_paths = []  # List to store the file paths

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)

print(file_paths)

import json
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Create a list to store the data
data = []
model = SentenceTransformer('model/model')

# Define the path for the processed data directory
processed_data_directory = 'processed_data'

# Iterate over the file paths
for file_path in file_paths:
    # Read the CSV file without column names
    df = pd.read_csv(file_path, header=None, names=['title', 'genre', 'summary'])
    #df = df[:100]

    # Extract the titles, genres, and summaries from the CSV
    titles = df['title'].tolist()
    genres = df['genre'].tolist()
    summaries = df['summary'].tolist()

    # Generate sentence embeddings for the summaries
    embeddings = model.encode(summaries)

    # Get the folder name from the file path
    genre = file_path.split("\\")[-1].split("_")[0]

    # Create the JSON filename
    json_filename = genre + '.json'

    # Iterate over the titles, genres, summaries, and embeddings
    for title, genre, summary, embedding in zip(titles, genres, summaries, embeddings):
        # Create a dictionary for each data entry
        entry = {
            'title': title,
            'genre': genre,
            'summary': summary,
            'embedding': embedding.tolist()  # Convert the embedding to a list for JSON serialization
        }
        # Append the entry to the data list
        data.append(entry)

    # Define the path for the JSON file in the processed data directory
    json_file_path = os.path.join(processed_data_directory, json_filename)

    # Write the data to a JSON file
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    # Clear the data list for the next file
    data = []