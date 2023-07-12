from sentence_transformers import SentenceTransformer, util
import os
import json
import time
import numpy as np
from flask import Flask, request, jsonify
import joblib



genre = "Action"

path = os.path.join("processed_data",genre+".json")

with open(path, 'r') as f:
    data = json.load(f) #contains entire file

print(data)