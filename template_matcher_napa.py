import json 


with open("coordinates_NAPA/Napa_template.json","r") as f:
    TEMPLATE = json.load(f)


def load_coordinates(path):
    with open(path,"r") as f:
        return json.load(f)
    


#word in coordinate bx
def words_in_box(words, box):
    
    selected = []
    for word in words : 

        # to debug
        # if word["text"] == "03/02/2026":
        #     print("FOUND DATE")
        #     print(word)

        #     print(
        #         box["x_min"] <= word["x0"] <= box["x_max"],
        #         box["y_min"] <= word["top"] <= box["y_max"]
        #     )

        if(box["x_min"] <= word["x0"] <= box["x_max"] and box["y_min"] <= word["top"] <= box["y_max"]):
            print(box["x_min"],box["x0"])
            selected.append(word)
        
        selected.sort(key=lambda x: x["x0"])
        return " ".join(["text"] for w in selected)
    
# grouping them into rows
def group_rows(words,tolerance = 8 ):
    rows = {}
    for word in words :
        #print(word)
        y = round(word["top"]/tolerance)*tolerance
        rows.setdefault(y, []).append(word)
    return rows

#products
def extract_products(words):
    table = TEMPLATE["product_table"]
    top = table["top"]
    bottom = table["bottom"]
    columns = table["columns"]
    table_words = []

    for word in words :
        #print(word)
        if top <= word["top"] <= bottom:
            table_words.append(word)
    rows = group_rows(table_words)
    products = []

    for row in rows.values():
        product = {
            'part_number' : " ",
            'description' : " ",
            "quantity" : " ",
            "price" : " ",
            "net" : " ",
            "line_total" : " "
        }
        row = sorted(row, key = lambda x:x["x0"])
        for word in row:
            x = word["x0"]
            if columns["part_number"]["x_min"] <= x <= columns["part_number"]["x_max"]:
                product["part_number"] += word["text"] + " "
            elif columns["description"]["x_min"] <= x <= columns['description']["x_max"]:
                product["description"] += word["text"] + " "
            elif columns["quantity"]["x_min"]<= x <= columns["quantity"]["x_max"]:
                product["quantity"] += word["text"] + ' '
            elif columns["price"]["x_min"] <= x <= columns["price"]['x_max']:
                product["price"] += word["text"] + ' '
            elif columns["line_total"]["x_min"] <= x <= columns["line_total"]["x_max"]:
                product["line_total"] += word["text"] + " "
        if  product["description"] != " ":
            for k in product:
                product[k] = product[k].strip()
            products.append(product)
    return products
    
def extract_napa_feilds(coord_path):
    words = load_coordinates(coord_path)
    result = {}
    #print("result")
    result["invoice_number"] = words_in_box( words , TEMPLATE["invoice_number"])
    result["invoice_date"] = words_in_box( words , TEMPLATE["invoice_date"])
    result["po_number"] = words_in_box( words , TEMPLATE["po_number"])
    result["subtotal"] = words_in_box( words , TEMPLATE["subtotal"])
    result["emmployee"] = words_in_box( words , TEMPLATE["tax"])
    result["total"] = words_in_box( words , TEMPLATE["invoice_total"])
    result["products"] = extract_products(words)
    return result