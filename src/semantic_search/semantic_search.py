from sentence_transformers import SentenceTransformer, util

'''
model = SentenceTransformer('model/model')

# Example sentences
sentence = ["Fight an entire army alone"]
sentence_2 = ["Always stand alone, against everyone, against anyone."]

# Generate sentence embeddings
embeddings = model.encode(sentence)
embeddings2 = model.encode(sentence_2)

#Compute cosine-similarities
cosine_scores = util.cos_sim(embeddings, embeddings2)
print(cosine_scores)
'''

import json
import time

# Start measuring time
start_time = time.time()
# Read the JSON file
with open('processed_data\Adventure.json', 'r') as f:
    data = json.load(f) #contains entire file

# Calculate the elapsed time
#elapsed_time = time.time() - start_time
#print("Time taken: {:.2f} seconds".format(elapsed_time))    #0.66 seconds

#Load model
model = SentenceTransformer('model/model')

#User generated prompt's embeddings
prompt = ["Masked vigilante fights crime undercover"]
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
import numpy as np

similarity_index_arr = np.array(similarity_index)
sorted_similarity_index_arr = similarity_index_arr[similarity_index_arr[:, 0].argsort()]
sorted_similarity_index = sorted_similarity_index_arr.tolist()

#Print top three results
print(f"Title: {data[int(sorted_similarity_index[999][1])]['_id']}\nSummary: {data[int(sorted_similarity_index[999][1])]['summary']}\n")
print(f"Title: {data[int(sorted_similarity_index[998][1])]['_id']}\nSummary: {data[int(sorted_similarity_index[998][1])]['summary']}\n")
print(f"Title: {data[int(sorted_similarity_index[997][1])]['_id']}\nSummary: {data[int(sorted_similarity_index[997][1])]['summary']}\n")


# Calculate the elapsed time
elapsed_time = time.time() - start_time
print("Time taken: {:.2f} seconds".format(elapsed_time))
