from pymongo import MongoClient
import json
#client = MongoClient("mongodb+srv://azwarshariq:e0mGo8aavNOudTqk@<cluster-url>")
#db = client['Genre']
#collection = db['Action']




from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://azwarshariq:e0mGo8aavNOudTqk@cluster.sfx9ced.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


db = client['Genre']
collection = db['Action']
# Retrieve all documents from the collection
documents = collection.find()

# Convert documents to a list
documents_list = list(documents)

print(documents_list[0])