from pdf_reader import extract_text
from vector_store import create_vector_store

text = extract_text("uploads/oops index.pdf")

print(create_vector_store(text))