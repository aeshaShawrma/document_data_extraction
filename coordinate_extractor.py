import pdfplumber
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path


def extract_coordinates(file_path):
    coordinates = []
    with pdfplumber.open(file_path) as pdf:
        searchable = pdf.pages[0].extract_words()
        if searchable:
            print("Searchable pdf")
            
            for page_num , page in enumerate(pdf.pages):
                words = page.extract_words()
                for word in words:
                    coordinates.append({
                        "page": page_num+1,
                        "text" : word["text"],
                        "x0" : word["x0"],
                        "x1" : word["x1"],
                        "top" : word["top"],
                        "bottom" : word["bottom"]
                    })
        else:
                print("Scanned PDF Usinf OCR")
                import fitz
                from PIL import Image

                doc = fitz.open(file_path)

                for page_num, page in enumerate(doc):   
                    pix = page.get_pixmap(dpi=300)

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                data = pytesseract.image_to_data(
                    image,
                    output_type=Output.DICT
                )

                for i in range(len(data["text"])):
                    if data["text"][i].strip():

                     coordinates.append({
                        "page": page_num,
                        "text": data["text"][i],
                        "x0": data["left"][i],
                        "top": data["top"][i],
                        "x1": data["left"][i] + data["width"][i],
                        "bottom": data["top"][i] + data["height"][i]
                    })

    return coordinates