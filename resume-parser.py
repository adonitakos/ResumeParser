from flask import Flask, request, render_template, send_from_directory
from firebase_admin import credentials, initialize_app, storage
import os
import re
import PyPDF2
import io

cred = credentials.Certificate("resumeparser-b078e-firebase-adminsdk-w3w9w-0ba829935b.json")
initialize_app(cred, {
    'storageBucket': 'resumeparser-b078e.appspot.com'
})

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
    bucket = storage.bucket()
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    return 'File uploaded successfully'

# LOCAL TEXT FILES IMPLEMENTATION
# def search_files(directory, keyword, results):
#     for file in os.listdir(directory):
#         if file.endswith(".txt"):
#             with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
#                 contents = f.read()
#                 matches = re.findall(keyword, contents, re.IGNORECASE)
#                 if matches:
#                     results.append(f"{file} contains the keyword {keyword} {len(matches)} times.")
#                 else:
#                     results.append(f"{file} does not contain the keyword {keyword}.")


# def search_files(bucket, keyword, results):
#     blobs = bucket.list_blobs()
#     for blob in blobs:
#         if blob.name.endswith(".txt"):
#             contents = blob.download_as_string().decode("utf-8")
#             matches = re.findall(keyword, contents, re.IGNORECASE)
#             if matches:
#                 results.append(f"{blob.name} contains the keyword {keyword} {len(matches)} times.")
#             else:
#                 results.append(f"{blob.name} does not contain the keyword {keyword}.")
                

def search_pdf_files(bucket, keyword, results):
    blobs = bucket.list_blobs()
    for blob in blobs:
        if blob.name.endswith(".pdf"):
            contents = blob.download_as_string()
            pdf = PyPDF2.PdfFileReader(io.BytesIO(contents))
            pdf_text = ""
            for page in range(pdf.numPages):
                pdf_text += pdf.getPage(page).extractText()
            matches = re.findall(keyword, pdf_text, re.IGNORECASE)
            if matches:
                results.append(f"{blob.name}: contains the keyword {keyword} {len(matches)} times.")
            else:
                results.append(f"{blob.name}: does NOT contain the keyword {keyword}.")
        


print("\n\n================== Welcome ==================\n\n")

# Example usage
directory = directory = os.path.join(os.getcwd(), 'text-resumes')

# LOCAL TEXT FILES IMPLEMENTATION
# @app.route('/search', methods=['POST'])
# def search():
#     keyword = request.form['keyword']
#     results = []
#     search_files(directory, keyword, results)
#     return render_template('index.html', results=results)

# @app.route('/search', methods=['POST'])
# def search():
#     keyword = request.form['keyword']
#     bucket = storage.bucket()
#     results = []
#     search_files(bucket, keyword, results)
#     return render_template('index.html', results=results)

@app.route('/search', methods=['POST'])
def search():
    try:
        keyword = request.form['keyword']
        bucket = storage.bucket()
        results = []
        search_pdf_files(bucket, keyword, results)
        return render_template('index.html', results=results)
    except Exception as e:
        return str(e)


# Running Flask web application
app.run(host='0.0.0.0', port=5000)