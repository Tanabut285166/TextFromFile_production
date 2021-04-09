from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

from . import text_extracter

app = Flask(__name__)


POPPLER_PATH = r"C:/Program Files/poppler-21.03.0/Library/bin"
TESSERACT_PATH = r"D:/ocr/Tesseract-OCR/tesseract.exe"

FILE_UPLOADS = r"D:\ocr\TextFromFile\src\upload"
ALLOWED_FILE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF", "PDF", "DOCX"]

fileReader = text_extracter.TextExtracter(poppler_path=POPPLER_PATH, tesseract_path=TESSERACT_PATH )

@app.route('/upload-docx', methods=[ 'POST',])
def upload_docx():
    result = ""
    if request.files:
        file_input = request.files["file"]

        if file_input.filename == "":
            return {"error": "No filename" }

        if not allowed_file(file_input.filename):
            return {"error": "That file extension is not allowed"}
        
        filename = secure_filename(file_input.filename)
        result += fileReader.read_docx(file_input)

        return jsonify(result)
    return {"error": "fail to read file"}

@app.route('/upload-pdf', methods=[ 'POST',])
def upload_pdf():
    result = ""
    if request.files:
        file_input = request.files["file"]

        if file_input.filename == "":
            return {"error": "No filename" }

        if not allowed_file(file_input.filename):
            return {"error": "That file extension is not allowed"}
        
        filename = secure_filename(file_input.filename)
        save_path = os.path.join(FILE_UPLOADS, filename)
        file_input.save(save_path)
        fileJPGNames = fileReader.convert_pdf_to_jpg(save_path,save=True)
        return {"ok": 200 }

    return {"eror" : "fail to read this file"}

def allowed_file(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in ALLOWED_FILE_EXTENSIONS:
        return True
    
    return False
