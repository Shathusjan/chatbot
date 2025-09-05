import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Load FAISS index and chunk mapping
index = faiss.read_index("faiss_index.bin")
with open("chunk_mapping.pkl", "rb") as f:
    chunk_mapping = pickle.load(f)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_context(query, top_k=3):
    """
    Generate embedding for the query, search FAISS index, and return relevant chunks.
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for idx in indices[0]:
        if idx < len(chunk_mapping):
            results.append(chunk_mapping[idx])
    return results

if __name__ == "__main__":
    test_query = "What is the capital of France?"
    contexts = retrieve_context(test_query, top_k=3)
    print("Retrieved contexts:")
    for i, context in enumerate(contexts, 1):
        print(f"{i}. {context}")
