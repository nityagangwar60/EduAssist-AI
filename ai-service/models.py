from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    conversations = relationship(
    "Conversation",
    back_populates="user",
    cascade="all, delete"
)
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    title = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="conversations"
    )

    chats = relationship(
        "ChatHistory",
        back_populates="conversation",
        cascade="all, delete"
    )
class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id")
    )
    conversation = relationship(
    "Conversation",
    back_populates="chats"
)
    question = Column(String)
    answer = Column(String)

    intent = Column(String)
    sentiment = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
class PDFDocument(Base):
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    filename = Column(String)

    vector_path = Column(String)

    chunks_path = Column(String)

    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

