FAQS = {
    "what is your name": "I am EduAssist AI, your student support assistant.",

    "who are you": "I am EduAssist AI developed to help students with academics, career guidance, and general queries.",

    "what is dbms": "DBMS (Database Management System) is software used to store, manage, and retrieve data efficiently.",

    "what is python": "Python is a high-level programming language widely used in AI, Machine Learning, Web Development, and Data Science.",

    "what is machine learning": "Machine Learning is a branch of Artificial Intelligence that enables computers to learn patterns from data.",

    "what is ai": "Artificial Intelligence is the simulation of human intelligence by machines.",

    "hello": "Hello! How can I help you today?",

    "hi": "Hi! Welcome to EduAssist AI.",

    "thanks": "You're welcome!",

    "thank you": "Happy to help!"
}


def search_faq(question):
    question = question.lower().strip()

    for key, value in FAQS.items():
        if key == question:          # exact match only
            return value

    return None