from docx import Document
from PyPDF2 import PdfFileReader
from unidecode import unidecode
from pdf2image import convert_from_path
from PIL import ImageDraw, Image, ImageGrab
import ntpath
import pytesseract
import os 

class TextExtracter:
    def __init__(self, poppler_path, tesseract_path):
        self.poppler_path = poppler_path #PDF to image converter's path
        self.tesseract_path = tesseract_path

        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path 
 
    def read_docx(self, filePath):
        result = ""
        document = Document(filePath)
        paragraphs = document.paragraphs

        for paragraph in paragraphs:
            result += paragraph.text

        return result

    def _name_from_path(self,path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def _trim_str(self, raw_txt):
        new_txt =""
        for i in range(len(raw_txt)):
            if ord(raw_txt[i]) != 32: #space
                new_txt += raw_txt[i]
            elif ord(raw_txt[i + 1] ) < 3585:  # not thai include space
                new_txt += raw_txt[i]

        return new_txt 

    def save(self, txt, path=""):
        f = open(f"{path}.txt", "w")
        f.write(txt)
        f.close()


    def convert_pdf_to_jpg(self, filePath, save=True):
        JPGNames = []
        dirName = os.path.dirname(filePath)
        fileName = self._name_from_path(filePath).replace(".pdf","")
        images = convert_from_path(filePath, poppler_path = self.poppler_path)
        
        for i in range(len(images)):
            JPGName = fileName + "_" + 'page'+ str(i) +'.jpg'
            JPGNames.append( JPGName )

            if(save):
                save_path = os.path.join(dirName, JPGName)
                images[i].save( save_path, 'JPEG' )
            
        return JPGNames 
    
    def extract_jpg_to_text(self, filePath):
        img = Image.open(filePath)
        result = pytesseract.image_to_string(img, lang='tha+eng')
        new_txt = self._trim_str(result)
        
        return new_txt