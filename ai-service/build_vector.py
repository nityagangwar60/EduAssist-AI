import os
from pdf_reader import extract_text
from vector_store import create_vector_store

pdf_path = "uploads/oops index.pdf"

if os.path.exists(pdf_path):
    text = extract_text(pdf_path)
    create_vector_store(text)
    print("Vector created")
else:
    print("No PDF found. Skipping vector creation.")