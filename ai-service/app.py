from httpcore import request
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserRegister, UserLogin, ChatRequest
from models import Conversation
from database import engine, Base, get_db
from models import User
from auth import hash_password, verify_password
from schemas import ChatRequest, ChatResponse
from models import ChatHistory
from intent import detect_intent
from vector_store import create_vector_store, search_vector
from chatbot import ask_ai
from sentiments import predict_sentiment
from fastapi import UploadFile, File
import shutil
from pdf_reader import extract_text

import os
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduAssist AI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "EduAssist AI Backend Running"}


@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Registration Successful"}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid Password")

    return {
    "message": "Login Successful",
    "id": db_user.id,
    "user": db_user.full_name,
    "email": db_user.email
}


@app.post("/new-conversation/{user_id}")
def new_conversation(user_id: int, db: Session = Depends(get_db)):

    conversation = Conversation(
        user_id=user_id,
        title="New Chat"
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "conversation_id": conversation.id
    }
@app.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    print("REQUEST =", request)
    print("USER ID =", request.user_id)
    # Check user exists
    user = db.query(User).filter(User.id == request.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if request.conversation_id is None:
        conversation = Conversation(
            user_id=request.user_id,
            title=request.question[:40]
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        request.conversation_id = conversation.id
    # Detect intent
    intent = detect_intent(request.question)

    # Detect sentiment
    sentiment = predict_sentiment(request.question)
    previous_chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == request.user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(5)
        .all()
    )

    memory = ""

    for chat in reversed(previous_chats):
        memory += f"""
User: {chat.question}
Assistant: {chat.answer}
"""

    # Search relevant context from uploaded PDFs
    context, sources = search_vector(request.question)

    # Get AI answer from OpenRouter using RAG
    answer = ask_ai(
        question=request.question,
        context=context,
        memory=memory    )

    # Save chat history
    chat = ChatHistory(
    user_id=request.user_id,
    conversation_id=request.conversation_id,
    question=request.question,
    answer=answer,
    intent=intent,
    sentiment=sentiment
)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return {
    "conversation_id": request.conversation_id,
    "intent": intent,
    "sentiment": sentiment,
    "answer": answer,
    "sources": sources
}
@app.get("/chat-history/{user_id}")
def get_chat_history(user_id: int, db: Session = Depends(get_db)):

    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )

    return {
        "history": conversations
    }


@app.delete("/chat-history/{user_id}")
def clear_chat_history(user_id: int, db: Session = Depends(get_db)):

    db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).delete()

    db.commit()

    return {
        "message": "All chats deleted successfully"
    }
@app.delete("/chat-history/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):

    chat = db.query(ChatHistory).filter(ChatHistory.id == chat_id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    db.delete(chat)
    db.commit()

    return {
        "message": "Chat deleted successfully"
    }
@app.get("/dashboard/{user_id}")
def dashboard(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_chats = db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).count()

    total_conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).count()

    total_pdfs = 0

    if os.path.exists("uploads"):
        total_pdfs = len(
            [f for f in os.listdir("uploads") if f.endswith(".pdf")]
        )

    return {
        "student_name": user.full_name,
        "email": user.email,
        "total_chats": total_chats,
        "total_conversations": total_conversations,
        "total_pdfs": total_pdfs,
        "knowledge_base": os.path.exists("vector.index")
    }
@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    print("\n========== PDF TEXT ==========")
    print(text[:3000])
    print("\n==============================\n")

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in PDF."
        )

    create_vector_store(
        text,
        file.filename
    )

    return {
        "message": "PDF uploaded successfully",
        "characters": len(text),
        "status": "Knowledge Base Updated"
    }
@app.get("/knowledge-base")
def knowledge_base():

    if os.path.exists("vector.index"):
        return {
            "status": "Knowledge Base Ready"
        }

    return {
        "status": "No Knowledge Base Found"
    }
@app.delete("/knowledge-base")
def clear_knowledge():

    if os.path.exists("vector.index"):
        os.remove("vector.index")

    if os.path.exists("chunks.pkl"):
        os.remove("chunks.pkl")

    return {
        "message": "Knowledge Base Deleted"
    }
@app.get("/health")
def health():

    return {
        "status": "running",
        "ai": "OpenRouter",
        "vector_db": os.path.exists("vector.index")
    }
@app.get("/pdfs")
def list_pdfs():

    upload_folder = "uploads"

    if not os.path.exists(upload_folder):
        return {
            "total_pdfs": 0,
            "files": []
        }

    files = os.listdir(upload_folder)

    pdfs = [file for file in files if file.endswith(".pdf")]

    return {
        "total_pdfs": len(pdfs),
        "files": pdfs
    }
@app.delete("/pdf/{filename}")
def delete_pdf(filename: str):

    file_path = os.path.join("uploads", filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="PDF not found"
        )

    os.remove(file_path)

    return {
        "message": "PDF deleted successfully"
    }
