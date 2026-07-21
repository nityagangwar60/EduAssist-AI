import joblib

model = joblib.load("sentiment_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


def predict_sentiment(text):
    X = vectorizer.transform([text])
    return model.predict(X)[0]