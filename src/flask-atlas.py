from sentence_transformers import SentenceTransformer, util
import os
import json
import time
import numpy as np
from flask import Flask, request, jsonify
import joblib
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load the model
model = SentenceTransformer('model')

# Create a new client and connect to the server
uri = "mongodb+srv://azwarshariq:e0mGo8aavNOudTqk@cluster.sfx9ced.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))


# Create a Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    
    #Get prompt-data
    data = request.json
    number_of_results = data['number_of_results']
    genre = data['genre']
    prompt = data['prompt']
    

    db = client['Genre']
    collection = db[genre]

    # Retrieve all documents from the collection
    data = collection.find()
    data = list(data)

    #User-generated prompt's embeddings
    prompt_embeddings = model.encode(prompt)

    similarity_index = []
    index_tracker = 0

    # Extract and search for maximum similarity
    for item in data:
        embeddings = item['embedding']
        
        #Calculate cosine_scores
        cosine_scores = util.cos_sim(prompt_embeddings, embeddings)
        cosine_scores = cosine_scores.tolist()[0]
        cosine_scores.append(index_tracker)
        similarity_index.append(cosine_scores)
        index_tracker += 1

    similarity_index_arr = np.array(similarity_index)
    sorted_similarity_index_arr = similarity_index_arr[similarity_index_arr[:, 0].argsort()]
    sorted_similarity_index = sorted_similarity_index_arr.tolist()

    n = int(number_of_results)  # Number of top results to return
    results = []

    for i in range(n):
        result_index = 999 - i  
        result = {
            'Summary': data[int(sorted_similarity_index[result_index][1])]['summary'],
            'Title': data[int(sorted_similarity_index[result_index][1])]['_id']
        }
        results.append(result)

    return jsonify(results)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True, threaded=True)
