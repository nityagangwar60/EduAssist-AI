def detect_intent(question: str):

    question = question.lower()

    academic_keywords = [
        "dbms", "python", "java", "os",
        "operating system", "computer network",
        "cn", "sql", "algorithm", "ml",
        "ai", "oops", "c language"
    ]

    quiz_keywords = [
        "quiz", "mcq", "questions", "test"
    ]

    career_keywords = [
        "career", "placement", "internship",
        "resume", "job", "interview", "roadmap"
    ]

    summary_keywords = [
        "summary", "summarize", "notes", "pdf"
    ]

    for word in academic_keywords:
        if word in question:
            return "Academic"

    for word in quiz_keywords:
        if word in question:
            return "Quiz"

    for word in career_keywords:
        if word in question:
            return "Career"

    for word in summary_keywords:
        if word in question:
            return "Summary"

    return "General"