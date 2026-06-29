import json

def find_value_after_label(coordinates,label):
    label_words = label.split()
    for i in range (len(coordinates)-len(label_words)):
        match = True

        for j in range(len(label_words)):
            if coordinates[i+j]["text"].lower() != label_words[j].lower():
                match = False
                break

        if match :
            return coordinates[i+len(label_words)["text"]]
    
    return None

def extract_napa_feilds(json_path):
    with open(json_path , "r") as f:
        coordinates = json.load(f)
    result ={}

    result["invoice_number"] = find_value_after_label( coordinates , "Invoice Number")
    result["invoice_date"]= find_value_after_label(coordinates , "Invoice Date")
    result["employee"] = find_value_after_label(coordinates , "Employee")
    result["po_number"] = find_value_after_label(coordinates , "PO")
    result["subtotal"] = find_value_after_label(coordinates , "Subtotal")
    result["total"] = find_value_after_label(coordinates , "Total")
    return result 

def group_rows(coordinates,tolerance = 5):
    rows = {}
    for word in coordinates :
        y = round(word["top"] / tolerance) * tolerance
        rows.setdefault(y , []).append(word)
    return rows

def extract_products(coordinates):
    rows = group_rows(coordinates)
    products = []
    for row in rows.values():
        text = " ".join(w["text"] for w in sorted(row, key = lambda x: x["x0"]))
        if "CMS" in text :
            products.append(text)

    return products