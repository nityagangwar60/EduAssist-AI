from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import joblib
import os

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_FILE = "vector.index"
CHUNKS_FILE = "chunks.pkl"


# -----------------------------
# Create / Update Vector Store
# -----------------------------
def create_vector_store(text,source):

    chunks = []

    # Better chunking
    for i in range(0, len(text), 400):
        chunk = text[i:i + 400].strip()
        if chunk:
            chunks.append({
    "text": chunk,
    "source": source
})

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
    texts,
    convert_to_numpy=True
    )

    dimension = embeddings.shape[1]

    # Existing vector store hai?
    if os.path.exists(INDEX_FILE) and os.path.exists(CHUNKS_FILE):

        index = faiss.read_index(INDEX_FILE)
        old_chunks = joblib.load(CHUNKS_FILE)

        index.add(embeddings)

        old_chunks.extend(chunks)

        joblib.dump(old_chunks, CHUNKS_FILE)
        faiss.write_index(index, INDEX_FILE)

    else:

        index = faiss.IndexFlatL2(dimension)

        index.add(embeddings)

        faiss.write_index(index, INDEX_FILE)
        joblib.dump(chunks, CHUNKS_FILE)

    return "Vector Store Updated Successfully"


# -----------------------------
# Search
# -----------------------------
def search_vector(question, top_k=3):

    if not os.path.exists(INDEX_FILE):
        return ""

    if not os.path.exists(CHUNKS_FILE):
        return ""

    index = faiss.read_index(INDEX_FILE)

    chunks = joblib.load(CHUNKS_FILE)

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )

    D, I = index.search(query_embedding, top_k)

    context = ""

    for idx in I[0]:

        if idx != -1:
            context += chunks[idx]["text"] + "\n\n"
    sources = []
    for idx in I[0]:
        if idx != -1:
            src = chunks[idx].get("source")
            if src and src not in sources:
                sources.append(src)

    return context, sources