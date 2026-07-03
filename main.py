import pdfplumber
import json
#from pdf2image import convert_from_path
import requests
import os
# from pdf2image import convert_from_path
from PIL import Image

import pytesseract 
pytesseract.pytesseract.tesseract_cmd = (
     r"C:\Users\Aesha.sharma\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)
from coordinate_extractor import extract_coordinates
from template_matcher_napa import extract_napa_feilds

file_path= r"C:\Users\Aesha.sharma\document_extraction\Sample_Template\NAPA invoices\NAPA_8.pdf"
text =""


extention = os.path.splitext(file_path)[1].lower()

if extention in [".png" , ".jpeg" , ".jpg"]:
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

    
    import fitz

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text()

    if len(text.strip()) < 50:
        print("no text founf. USING OCR...")

        for page in doc:
            pix = page.get_pixmap(dpi=300)      #taking photo of the page

            img = Image.frombytes(              # converts pymupdf raw img into a normal pil image
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            text += pytesseract.image_to_string(img) + "\n"

else :
    print("unsupported file type")
    exit()

print("\n                EXTRACTED TEXT                       \n ")
print(text[:3000])

coordinates = extract_coordinates(file_path)
print(type(coordinates))
#print(coordinates[:50])
with open("coordinates_NAPA/Napa_8.json","w") as f:
    json.dump(coordinates,f,indent =4)
print("coordinates saved successfullty")
    
result = extract_napa_feilds("coordinates_NAPA/NAPA_8.json")
print("\n extracted data\n")
print(json.dumps(result,indent=4))
# prompt = f'''
#     You are an invoice data extraction system.
#     Extract only values explicitly present int the document.property
#     Do not calculate. 
#     do not infer.
#     do not estimate.
#     Return valid JSON only
#     feilds must be : 
#     - Invoice Number
#     - Date Issued
#     - Date Due
#     - Billing Address
#     - Shipping Address
#     -    Items: part number ,Description, Quantity, core price , total price, 
#     - net total  ,tax

#     Document:
#     {text}
#    '''

# #calling llama

# response = requests.post(                       #sending prompt to server
#     "http://localhost:11434/api/generate",
#     json={
#         "model" : "llama3",
#         "prompt" : prompt ,
#         "stream" : False
#     }
# )

# result = response.json()["response"]

# print("LLAMA Output")
# print(result)