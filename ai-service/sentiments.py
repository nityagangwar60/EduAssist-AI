import os
import joblib

vectorizer = None
model = None

if os.path.exists("vectorizer.pkl") and os.path.exists("sentiment_model.pkl"):
    vectorizer = joblib.load("vectorizer.pkl")
    model = joblib.load("sentiment_model.pkl")
def predict_sentiment(text):

    if vectorizer is None or model is None:
        return "Neutral"

    vector = vectorizer.transform([text])
    prediction = model.predict(vector)

    return prediction[0]