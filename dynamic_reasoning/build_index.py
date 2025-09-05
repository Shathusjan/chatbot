import json
import faiss
import numpy as np
from openai import OpenAI
import os
import pickle
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Load environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

# Load cleaned knowledge
with open("../scrape/knowledge_clean.json", "r", encoding="utf-8") as f:
    data = json.load(f)

chunks = data.get("chunks", [])
if not chunks:
    raise ValueError("No chunks found in knowledge_clean.json")

print(f"Loaded {len(chunks)} chunks from knowledge_clean.json")

# Create embeddings
embeddings = []
for i, chunk in enumerate(chunks):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    vector = response.data[0].embedding
    embeddings.append(vector)

embeddings = np.array(embeddings, dtype="float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index
faiss.write_index(index, "faiss_index.idx")

# Save mapping (id -> text)
with open("chunk_mapping.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("✅ FAISS index and mapping saved successfully!")