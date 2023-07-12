from sentence_transformers import SentenceTransformer, util
import os
import json
import time
import numpy as np
from flask import Flask, request, jsonify
import joblib

# Load the vectorizer and model
model = SentenceTransformer('model/model')

# Create a Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    
    data = request.json
    genre = data['genre']
    prompt = data['prompt']
    
    #Path to Genre file
    path = os.path.join("processed_data",genre+".json")

    #User-geenrated prompt's embeddings
    prompt_embeddings = model.encode(prompt)

    #Opening relevant file
    with open(path, 'r') as f:
        data = json.load(f) #contains entire file

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

    #Print top three results
    #print(f"Title: {data[int(sorted_similarity_index[999][1])]['_id']}\nSummary: {data[int(sorted_similarity_index[999][1])]['summary']}\n")
    #print(f"Title: {data[int(sorted_similarity_index[998][1])]['_id']}\nSummary: {data[int(sorted_similarity_index[998][1])]['summary']}\n")
    #print(f"Title: {data[int(sorted_similarity_index[997][1])]['_id']}\nSummary: {data[int(sorted_similarity_index[997][1])]['summary']}\n")


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
