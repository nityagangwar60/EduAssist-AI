from pdf_reader import extract_text

text = extract_text("uploads/oops index.pdf")

print(text[:1000])