import pdfplumber
from pdf2image import convert_from_path
import requests
import os
from pdf2image import convert_from_path
from PIL import Image

import pytesseract 
pytesseract.pytesseract.tesseract_cmd = (
     r"C:\Users\Aesha.sharma\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)



file_path= r"C:\Users\Aesha.sharma\document_extraction\data\invoices\invoices\Screenshot 2026-06-25 052808.png"

text =""

extention = os.path.splitext(file_path)[1].lower()

if extention in [".png" , "jpeg" , "jpg"]:
    print("Image detected. Using OCR....")
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image) 

elif extention == ".pdf":
    print("pdf detected ....")
    try:
        with pdfplumber.open(file_path) as pdf:  #open and closing file 'with open(file) as f:'

            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text+=page_text +"\n"
    except Exception as e:
        print("PDF extraction error :",e)

    if len(text.strip()) < 50:
        print("no text founf. USING OCR...")

        pages = convert_from_path(file_path)
        for page in pages:
            page_text = pytesseract.image_to_string(page)
            text += page_text +"\n"

else :
    print("unsupported file type")
    exit()

print("  \n                EXTRACTED TEXT                       \n ")
print(text[:3000])

prompt = f'''
    You are an invoice data extraction system.
    Extract only values explicitly present int the document.property
    Do not calculate. 
    do not infer.
    do not estimate.
    Return valid JSON only.property
    Document:
   '''

#calling llama

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model" : "llama3",
        "prompt" : prompt ,
        "stream" : False
    }
)

result = response.json()["response"]

print("LLAMA Output")
print(result)