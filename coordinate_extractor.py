import pdfplumber

def extract_coordinates(pdf_path):
    coordinates = []
    with pdfplumber.open(pdf_path) as pdf:
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
    return coordinates