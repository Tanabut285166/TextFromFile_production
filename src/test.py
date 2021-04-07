from text_extracter import TextExtracter
import numpy as np
import matplotlib as mpl

poppler_path= r"C:/Program Files/poppler-21.03.0/Library/bin"
tesseract_path= r"D:/ocr/Tesseract-OCR/tesseract.exe"
fileReader = TextExtracter(poppler_path=poppler_path, tesseract_path=tesseract_path )

def ReadDocx(): 
    path = "../asset/ocr-dataset/docx/dummyDoc2.docx"
    doc = fileReader.read_docx(path)
    return doc

def convertPDFToJpg():
    path = "../asset/ocr-dataset/pdf/MCC_1762.pdf"
    fileJPGNames = fileReader.convert_pdf_to_jpg(path,save=False)
    return fileJPGNames

def convertJpgToText():
    path = "../asset/ocr-dataset/images/MCC_1762_page0.jpg"
    text = fileReader.extract_jpg_to_text(path)
    fileReader.save(text)

    return text
    


def testCase():
    doc = ReadDocx()
    if (doc):
        print("read doc is pass")
    else:
        print("read doc is fail")

    images = convertPDFToJpg()
    if (images):
        print("convert pdf to jpg is pass")
    else:
        print("convert pdf to jpg is fail")

    text = convertJpgToText()
    if (text):
        print("convert jpg to text is pass")
    else:
        print("convert jpg to text is fail")

    



if __name__ == '__main__':
    testCase()