from flask import Flask, request, render_template
import fitz  # PyMuPDF for PDF Extraction
import spacy
from textblob import TextBlob
import os

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
keywords = ["Python", "Data Science", "AI", "Machine Learning", "HTML", "CSS", "JavaScript"]

def extract_text(file):
    text = ""
    
    # Save the uploaded file temporarily
    temp_path = os.path.join('uploads', file.filename)  # Fixed syntax error
    file.save(temp_path)

    print(f"Saved file size: {os.path.getsize(temp_path)} bytes")  # Log file size

    pdf_file = fitz.open(temp_path)

    print(f"Extracting text from: {temp_path}")  # Debugging statement

    for page in pdf_file:
        text += page.get_text()
    print(f"Extracted text: {text}")  # Debugging statement
    return text

def check_grammar(text):
    blob = TextBlob(text)
    mistakes = blob.correct()
    return mistakes

def analyze_keywords(text):
    found = [word for word in keywords if word.lower() in text.lower()]
    return found

@app.route('/')
def index():
    print("Received request for index page")  # Debugging statement
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return "❌ No file part in request!"

    file = request.files['resume']
    filename = file.filename

    if filename == '':
        return "❌ No file selected!"

    if file and filename.endswith('.pdf'):
        text = extract_text(file)
        if not text.strip():
            return "❌ The extracted text is empty!"

        grammar = check_grammar(text)
        matched_keywords = analyze_keywords(text)
        score = len(matched_keywords) * 10

        return f"""
        🎯 Resume Analysis Report:<br>
        ✅ Keywords Matched: {matched_keywords} <br>
        📝 Grammar Suggestions: {grammar} <br>
        🔥 Final Score: {score}/100
        """
    else:
        return "❌ Please upload PDF files only!"


if __name__ == "__main__":
    app.run(debug=True)
