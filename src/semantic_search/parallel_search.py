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
prompt = ["Fight an entire army alone"]
prompt_embeddings = model.encode(prompt)

similarity_index = []
index_tracker = 0
temp = []
from joblib import Parallel, delayed
import numpy as np
from joblib import Parallel, delayed
import numpy as np

def process_chunk(chunk, prompt_embeddings, chunk_start_index):
    temp = []
    for index, item in enumerate(chunk):
        index_tracker = chunk_start_index * len(chunk) + index
        embeddings = item['embedding']

        # Calculate cosine_scores
        cosine_scores = util.cos_sim(prompt_embeddings, embeddings)
        cosine_scores = cosine_scores.tolist()[0]
        cosine_scores.append(index_tracker)
        temp.append(cosine_scores)
    return temp

data_chunks = np.array_split(data, 4)

results = Parallel(n_jobs=4)(delayed(process_chunk)(chunk, prompt_embeddings, chunk_start_index)
                             for chunk_start_index, chunk in enumerate(data_chunks))

# Combine the results from all threads
similarity_index = []
for thread_result in results:
    similarity_index.extend(thread_result)

# Print the combined results
print(similarity_index)


# Calculate the elapsed time
elapsed_time = time.time() - start_time
print("Time taken: {:.2f} seconds".format(elapsed_time))
