import os

directory = 'data'  # Path to the directory

file_paths = [] 

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)

print(file_paths)

import json
import pandas as pd
from sentence_transformers import SentenceTransformer, util


data = []
model = SentenceTransformer('model/model')


processed_data_directory = 'processed_data'

# Iterate over the file paths
for file_path in file_paths:
    df = pd.read_csv(file_path, header=None, names=['title', 'genre', 'summary'])

    titles = df['title'].tolist()
    genres = df['genre'].tolist()
    summaries = df['summary'].tolist()

    # Generate sentence embeddings for the summaries
    embeddings = model.encode(summaries)
    genre = file_path.split("\\")[-1].split("_")[0]
    json_filename = genre + '.json'

    for title, genre, summary, embedding in zip(titles, genres, summaries, embeddings):
        entry = {
            '_id': title,
            'genre': genre,
            'summary': summary,
            'embedding': embedding.tolist() 
        }
        
        data.append(entry)

    # Path of the JSON file in the processed data directory
    json_file_path = os.path.join(processed_data_directory, json_filename)
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    
    data = []