from sentence_transformers import SentenceTransformer, util

'''
model_name = 'all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

model.save('model/model')

'''

# Load the saved model
model = SentenceTransformer('model/model')

# Example sentences
sentences = [
    'I enjoy taking long walks on the beach.',
    'The weather is beautiful today.',
    'Machine learning is an exciting field of study.',
]

# Generate sentence embeddings
embeddings = model.encode(sentences)

# Print the embeddings
for sentence, embedding in zip(sentences, embeddings):
    print(f"Sentence: {sentence}")
    print(f"Embedding: {embedding}\n")
