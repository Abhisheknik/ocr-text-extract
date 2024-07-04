import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError, PDFSyntaxError

# Set the TESSDATA_PREFIX environment variable (for Tesseract OCR)
os.environ['TESSDATA_PREFIX'] = 'C:\\Program Files (x86)\\Tesseract-OCR\\'

# Set the Tesseract executable path (adjust for your installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# Add Poppler bin directory to PATH
os.environ["PATH"] += os.pathsep + r'C:\\poppler\\24.02.0\\bin'  # Replace with your Poppler bin directory

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image '{image_path}': {e}")
        return ""

def convert_pdf_to_images(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        return images
    except PDFPageCountError as pe:
        print(f"Error extracting text from PDF '{pdf_path}': {pe}")
        return []
    except PDFSyntaxError as se:
        print(f"Syntax error in PDF '{pdf_path}': {se}")
        return []
    except Exception as e:
        print(f"Error converting PDF to images '{pdf_path}': {e}")
        return []

def extract_text_from_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF '{pdf_path}': {e}")
        return ""
