import json
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from google.generativeai import GenerativeModel

MEMORY_PATH = "memory/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {"past_queries": []}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=4)

def embed_text(text):
    model = GenerativeModel("models/text-embedding-004")
    embedding = model.embed_content(text=text)["embedding"]
    return np.array(embedding)

def search_memory(query, top_k=3):
    memory = load_memory()
    if not memory["past_queries"]:
        return []

    query_vec = embed_text(query).reshape(1, -1)
    similarities = []

    for item in memory["past_queries"]:
        text = item["text"]
        vec = np.array(item["embedding"]).reshape(1, -1)
        score = cosine_similarity(query_vec, vec)[0][0]
        similarities.append((score, text))

    similarities.sort(reverse=True)
    return [item[1] for item in similarities[:top_k]]

def store_memory(text):
    memory = load_memory()
    embedding = embed_text(text).tolist()
    memory["past_queries"].append({"text": text, "embedding": embedding})
    save_memory(memory)
