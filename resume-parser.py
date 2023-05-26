from flask import Flask, request, render_template, send_from_directory, redirect
import re
import PyPDF2
from docx import Document
import io
import os 
import time

# resumes folder directory
directory = os.path.join(os.getcwd(), 'resumes')

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading (corresponding to form in HTML)
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(directory, filename)
    file.save(file_path)
    return 'File uploaded successfully'
 
# LOCAL TEXT FILES IMPLEMENTATION
def search_text_files(directory, keyword, results):
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
                contents = f.read()
                matches = re.findall(keyword, contents, re.IGNORECASE)
                if matches:
                    results.append(f"{file} contains the keyword {keyword} {len(matches)} times.")
                else:
                    results.append(f"{file} does not contain the keyword {keyword}.")

# LOCAL PDF FILES IMPLEMENTATION
def search_pdf_files(directory, keyword, results):
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            file_path = os.path.join(directory, file)
            with open(file_path, 'rb') as f:
                pdf = PyPDF2.PdfFileReader(f)
                pdf_text = ""
                for page in range(pdf.numPages):
                    pdf_text += pdf.getPage(page).extractText()
                matches = re.findall(keyword, pdf_text, re.IGNORECASE)
                if matches:
                    results.append(f"{file}: contains the keyword {keyword} {len(matches)} times.")
                else:
                    results.append(f"{file}: does NOT contain the keyword {keyword}.")
                    
# LOCAL WORD DOC/DOCX FILES IMPLEMENTATION
def search_word_docs(directory, keyword, results):
    for file in os.listdir(directory):
        if file.endswith(".doc") or file.endswith(".docx"):
            file_path = os.path.join(directory, file)
            doc = Document(file_path)
            doc_text = ""
            for para in doc.paragraphs:
                doc_text += para.text
            matches = re.findall(keyword, doc_text, re.IGNORECASE)
            if matches:
                results.append(f"{file}: contains the keyword {keyword} {len(matches)} times.")
            else:
                results.append(f"{file}: does NOT contain the keyword {keyword}.")

print("\n\n================== Welcome ==================\n\n")

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    results = []
    search_text_files(directory, keyword, results)
    search_pdf_files(directory, keyword, results)
    search_word_docs(directory, keyword,results)
    return render_template('index.html', results=results)

# Running Flask web application
app.run(host='0.0.0.0', port=5000)