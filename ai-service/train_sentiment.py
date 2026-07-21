from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Training data
texts = [
    "I am happy",
    "This is amazing",
    "Thank you",
    "I love learning",

    "I am sad",
    "I am stressed",
    "I failed my exam",
    "I hate studying",

    "What is Python?",
    "Explain DBMS",
    "What is AI?",
    "Tell me about machine learning"
]

labels = [
    "Positive",
    "Positive",
    "Positive",
    "Positive",

    "Negative",
    "Negative",
    "Negative",
    "Negative",

    "Neutral",
    "Neutral",
    "Neutral",
    "Neutral"
]

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

joblib.dump(model, "sentiment_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully!")