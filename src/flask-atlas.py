from sentence_transformers import SentenceTransformer, util
import os
import json
import time
import numpy as np
from flask import Flask, request, jsonify
import joblib
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Load the vectorizer and model
model = SentenceTransformer('model/model')

#Atlas connection
uri = "mongodb+srv://azwarshariq:e0mGo8aavNOudTqk@cluster.sfx9ced.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


# Create a Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    
    data = request.json
    genre = data['genre']
    prompt = data['prompt']
    

    db = client['Genre']
    collection = db[genre]

    # Retrieve all documents from the collection
    data = collection.find()

    # Convert documents to a list
    data = list(data)

    #User-geenrated prompt's embeddings
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

    #print(similarity_index)


    #Sort the similarity_index
    similarity_index_arr = np.array(similarity_index)
    sorted_similarity_index_arr = similarity_index_arr[similarity_index_arr[:, 0].argsort()]
    sorted_similarity_index = sorted_similarity_index_arr.tolist()

    #Return top 3 results
    return jsonify({'Summary': data[int(sorted_similarity_index[999][1])]['summary'],
                    'Title': data[int(sorted_similarity_index[999][1])]['_id'],
                    },
                    {'Summary': data[int(sorted_similarity_index[998][1])]['summary'],
                    'Title': data[int(sorted_similarity_index[998][1])]['_id'],
                    },
                    {'Summary': data[int(sorted_similarity_index[997][1])]['summary'],
                    'Title': data[int(sorted_similarity_index[997][1])]['_id'],
                    },)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True, threaded=True)
