from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

VECTORIZER_FILE = "vectorizer.pkl"
CHUNKS_FILE = "chunks.pkl"


def create_vector_store(text, source):

    chunks = []

    for i in range(0, len(text), 400):
        chunk = text[i:i+400].strip()

        if chunk:
            chunks.append({
                "text": chunk,
                "source": source
            })

    if os.path.exists(CHUNKS_FILE):
        old_chunks = joblib.load(CHUNKS_FILE)
        old_chunks.extend(chunks)
        chunks = old_chunks

    texts = [c["text"] for c in chunks]

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(texts)

    joblib.dump(vectorizer, VECTORIZER_FILE)
    joblib.dump((vectors, chunks), CHUNKS_FILE)

    return "Vector Store Updated Successfully"


def search_vector(question, top_k=3):

    if not os.path.exists(CHUNKS_FILE):
        return "", []

    vectorizer = joblib.load(VECTORIZER_FILE)

    vectors, chunks = joblib.load(CHUNKS_FILE)

    query = vectorizer.transform([question])

    scores = cosine_similarity(query, vectors)[0]

    top = scores.argsort()[-top_k:][::-1]

    context = ""

    sources = []

    for idx in top:

        context += chunks[idx]["text"] + "\n\n"

        src = chunks[idx]["source"]

        if src not in sources:
            sources.append(src)

    return context, sources