import os
import json
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def normalize_chunk(chunk):
    """Normalize chunk formats into plain text."""
    if isinstance(chunk, dict):
        if "text" in chunk:
            return str(chunk["text"])
        return " ".join(str(v) for v in chunk.values())
    elif isinstance(chunk, list):
        return " ".join(str(item) for item in chunk)
    else:
        return str(chunk)

# -------------------- JSON-based FAISS + SentenceTransformer --------------------

# Load knowledge_clean.json and extract chunks
with open("scrape/knowledge_clean.json", "r", encoding="utf-8") as f:
    knowledge_data = json.load(f)

# Extract chunks from possible keys
if isinstance(knowledge_data, dict):
    if "chunks" in knowledge_data:
        chunks = knowledge_data["chunks"]
    elif "data" in knowledge_data:
        chunks = knowledge_data["data"]
    else:
        # If dict but no known keys, treat as single chunk
        chunks = [knowledge_data]
elif isinstance(knowledge_data, list):
    chunks = knowledge_data
else:
    raise ValueError("knowledge_clean.json format not recognized: expected dict or list.")

if not chunks:
    raise ValueError("No chunks found in knowledge_clean.json.")

# Normalize chunks
chunk_texts = [normalize_chunk(chunk) for chunk in chunks]

# Lazy-loaded SentenceTransformer model
sbert_model = None

def get_sbert_model():
    global sbert_model
    if sbert_model is None:
        sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
    return sbert_model

# Initialize SentenceTransformer model and compute embeddings for chunks
model = get_sbert_model()
chunk_embeddings = model.encode(
    chunk_texts, convert_to_numpy=True, normalize_embeddings=True
)
embedding_dim_chunks = chunk_embeddings.shape[1]

# Build FAISS index
index_chunks = faiss.IndexFlatIP(embedding_dim_chunks)
index_chunks.add(chunk_embeddings)

def retrieve_relevant_chunks(query, k=5):
    """Retrieve top-k matching chunks."""
    model = get_sbert_model()
    query_embedding = model.encode(
        [query], convert_to_numpy=True, normalize_embeddings=True
    )
    distances, indices = index_chunks.search(query_embedding, k)
    results = [chunk_texts[i] for i in indices[0]]
    return results

def ask_bot(query):
    """Answer user query using only knowledge_clean.json context."""
    try:
        relevant_chunks = retrieve_relevant_chunks(query, k=5)
        context = "\n\n".join(relevant_chunks)

        system_prompt = (
            "You are a helpful assistant. Use only the CONTEXT below to answer the user’s question.\n"
            "Guidelines:\n"
            "- If the information in the context appears as a list (for example, separated by commas, dashes, semicolons, or newlines), present it as bullet points, one item per line.\n"
            "- Keep your answers concise: use at most 1–2 sentences before any list.\n"
            "- Avoid repeating identical or similar details.\n"
            "- Do not invent or add any information not present in the context.\n"
            "- If the answer cannot be found in the context, reply: 'I don’t know based on the provided information.'\n"
            "- Ensure your formatting is clear and suitable for any topic or industry.\n\n"
            f"CONTEXT:\n{context}"
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0,
        )

        # Some SDKs return dict-style objects, handle both safely
        choice = completion.choices[0]
        if hasattr(choice.message, "content"):
            return choice.message.content.strip()
        elif isinstance(choice.message, dict) and "content" in choice.message:
            return choice.message["content"].strip()
        else:
            return "I don't know based on the provided information."

    except Exception as e:
        print(f"🔥 Error in ask_bot: {e}")
        return "Sorry, I had trouble processing that request."


# Alias for backward compatibility
retrieve_context = retrieve_relevant_chunks