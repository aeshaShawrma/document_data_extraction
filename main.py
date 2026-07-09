import pdfplumber
import json
#from pdf2image import convert_from_path
import requests
import os
# from pdf2image import convert_from_path
from PIL import Image

import pytesseract 
pytesseract.pytesseract.tesseract_cmd = (
     r"C:/Users/Aesha.sharma/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
)
from coordinate_extractor import extract_coordinates
# from template_matcher_napa import extract_napa_feilds
# from template_matcher_autozone import extract_autozone_feilds
# from template_matcher_us_autoforce import extract_autoforce_feilds
# from template_matcher_oreilly import extract_oreilly_feilds
# from template_matcher_car_quest import extract_car_quest_feilds
# from template_matcher_worldpac import extract_worldpac_feilds
# from template_matcher_advanceautoparts import extract_advanceautoparts_feilds
# from template_matcher_autoparts_warehouse import extract_autoparts_warehouse_feilds




file_path= r"C:/Users/Aesha.sharma/document_extraction/Sample_Template/autoparts warehouse/invoice_19IV520589_page_1.pdf"


extention = os.path.splitext(file_path)[1].lower()

if extention in [".png" , ".jpeg" , ".jpg"]:
    print("Image detected. Using OCR....")
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image) 

elif extention == ".pdf":
    text = ""
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

    
    from vendor_detector import detect_vendor

    page_vendors = {}

    for page_num, page in enumerate(doc, start=1):

        page_text = page.get_text()

        vendor = detect_vendor(page_text)

        page_vendors[page_num] = vendor

    print(page_vendors)


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

def get_coordinates_for_pages(
        coordinates,
        page_numbers):

    return [

        word

        for word in coordinates

        if word["page"] in page_numbers
    ]

def build_vendor_groups(pages):

    groups = []

    current_vendor = None
    current_pages = []

    for page_no in sorted(pages.keys()):

        words = pages[page_no]

        page_text = " ".join(
            word["text"]
            for word in words
        )

        vendor = detect_vendor(page_text)

        if vendor != current_vendor:

            if current_pages:

                groups.append({
                    "vendor": current_vendor,
                    "pages": current_pages
                })

            current_vendor = vendor
            current_pages = [page_no]

        else:

            current_pages.append(page_no)

    if current_pages:

        groups.append({
            "vendor": current_vendor,
            "pages": current_pages
        })

    return groups

def group_coordinates_by_page(coordinates):

    pages = {}

    for word in coordinates:

        page_no = word["page"]

        if page_no not in pages:
            pages[page_no] = []

        pages[page_no].append(word)

    return pages

pages = group_coordinates_by_page(coordinates)
from invoice_detector import get_invoice_number

for page_no , words in pages.items():
    page.text="".join(w["text"] for w in words)

    vendor = detect_vendor(page_text)

    invoice_no = get_invoice_number(
        page_text
    )

    print(
        f"Page {page_no}"
        f" Vendor={vendor}"
        f" Invoice={invoice_no}"
    )

vendor_groups = build_vendor_groups(pages)

print(json.dumps(vendor_groups, indent=4))

from vendor_detector import detect_vendor_from_coordinates

for page_no, words in pages.items():

    page_text = " ".join(
        w["text"] for w in words
    )

    vendor = detect_vendor(page_text)

    print(f"Page {page_no}: {vendor}")


vendor = detect_vendor_from_coordinates(coordinates)

print(f"Vendor detected : {vendor}")

print(type(coordinates))
#print(coordinates[:50])
coordinate_file = "coordinates/current_invoice.json"
with open(coordinate_file,"w") as f:
    json.dump(coordinates,f,indent =4)
print("coordinates saved successfullty")


from extractor_registry import EXTRACTORS

extractor = EXTRACTORS.get(vendor)
result = []
if extractor:

    # result = extractor(
    #     "coordinates/coordinates_autoparts_warehouse/11.json"
    # )

    result = extractor(coordinate_file)
    print(json.dumps(result, indent=4))

else:
    print("Vendor not supported")



from output_normalizer import normalize
final_output = []

for invoice in result:

    final_output.append(
        normalize(invoice, vendor)
    )

with open("final_output.json","w") as f:

    json.dump(
        final_output,
        f,
        indent=4
    )

# # _______________________ NAPA ___________________________________
# result = extract_napa_feilds("coordinates/coordinates_NAPA/coordinates_autozone/1.json")
# print("\n extracted data\n")
# print(json.dumps(result,indent=4))

# #________________________Autozone_____________________________________
# result = extract_autozone_feilds("coordinates/coordinates_NAPA/coordinates_autozone/1.json")
# print("\n extracted data\n")
# print(json.dumps(result,indent=4))
# with open("extracted_data/autozone/1.json", "w") as f:
#     json.dump(result, f, indent = 4)
# print("extraction saved sucessfully")

# #_________________________US AutoForce_________________________________________ (Not working)
# result = extract_autoforce_feilds("coordinates/coordinates_US_autoforce/1.json")
# print("\n extracted data \n")
# print(json.dumps(result,indent=4))
# with open("extracted_data/US_autoforce_1.json", "w") as f:
#     json.dump(result,f, indent=4)

# #________________________ORielly_____________________________________________________
# result = extract_oreilly_feilds("coordinates/coordinates_o'reilly/1.json")
# print("\n extracted data \n")
# print(json.dumps(result,indent=4))
# with open("extracted_data/oreilly/1.json","w") as f:
#     json.dump(result,f,indent=4)

# #________________________Car_Quest_____________________________________________________
# result = extract_car_quest_feilds("coordinates/coordinates_car_quest/1.json")
# print("\n extracted data \n")
# print(json.dumps(result , indent =4))
# with open("extracted_data/car_quest/1.json","w") as f:
#     json.dump(result,f,indent=4)

# #________________________Worldpac_____________________________________________________
# result = extract_worldpac_feilds("coordinates/coordinates_worldpac/1.json")
# print("\n extracted data \n")
# print(json.dumps(result , indent =4))
# with open("extracted_data/worldpac/1.json","w") as f:
#     json.dump(result,f,indent=4)

# #___________________________Advance Auto Parts___________________________________________

# result = extract_advanceautoparts_feilds("coordinates/coordinates_advanceautoparts/1.json")
# print("\n extracted data \n")
# print(json.dumps(result , indent =4))
# with open("extracted_data/advance_autoparts/1.json","w") as f:
#     json.dump(result,f,indent=4)

# #__________________________Autoparts Warehouse_____________________________________________

# result = extract_autoparts_warehouse_feilds("coordinates/coordinates_autoparts_warehouse/1.json")
# print("\n extracted data \n")
# print(json.dumps(result,indent = 4))
# with open("extracted_data/autoparts_warehouse/1.json","w") as f:
#     json.dump(result,f,indent=4)
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