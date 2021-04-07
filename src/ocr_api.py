from . import text_extracter
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

MAX_FILE_FILESIZE = 0.5 * 1024 * 1024
FILE_UPLOADS = r"D:\ocr\TextFromFile\src\upload"
ALLOWED_FILE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF", "DOCX", "DOC", "PDF"]

poppler_path= r"C:/Program Files/poppler-21.03.0/Library/bin"
tesseract_path= r"D:/ocr/Tesseract-OCR/tesseract.exe"
fileReader = text_extracter.TextExtracter(poppler_path=poppler_path, tesseract_path=tesseract_path )

@app.route("/upload-image", methods=["POST"])
def upload_image():
    if request.files :
        image = request.files["file"]

        if image.filename == "":
            return {"error": "No filename"}

        if not allowed_image(image.filename):
            return {"error": "That file extension is not allowed"}
        
        filename = secure_filename(image.filename)
        image.save(os.path.join(FILE_UPLOADS, filename))
        return {"ok":200}

    return {"error": "can't extract text from this file"}

@app.route("/upload-docx", methods=["POST"])
def upload_docx():
    if request.files:
        docx = request.files["file"]

        if docx.filename == "":
            return {"error": "No filename"}

        if not allowed_image(docx.filename):
            return {"error": "That file extension is not allowed"}
        
        txt = fileReader.read_docx(docx)
        return jsonify(txt)

    return {"error": "fail to read file"}


@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    txt = ""
    if request.files:
        pdf = request.files["file"]

        if pdf.filename == "":
            return {"error": "No filename"}

        if not allowed_image(pdf.filename):
            return {"error": "That file extension is not allowed"}
      
        filename = secure_filename(pdf.filename)
        path = os.path.join(FILE_UPLOADS, filename)

        pdf.save(path)
        imagesName = fileReader.convert_pdf_to_jpg(filePath=path, save=True )

        for i in range(len(imagesName)):
            print("--------------" + os.path.join(FILE_UPLOADS, imagesName[i]))
            txt += fileReader.extract_jpg_to_text(os.path.join(FILE_UPLOADS, imagesName[i]))

        return jsonify(txt)
        
    return {"error": "fail to read file"}


def allowed_image_filesize(filesize):
    if int(filesize) <= MAX_FILE_FILESIZE:
        return True
    return False

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in ALLOWED_FILE_EXTENSIONS:
        return True
    return False
