import json 


with open("coordinates_NAPA/Napa_template.json","r") as f:
    TEMPLATE = json.load(f)


def load_coordinates(path):
    with open(path,"r") as f:
        return json.load(f)
    


#word in coordinate bx
def words_in_box(words, box):
    
    selected = []
    #print("TOTAL WORDS", len(words))
    for word in words : 

        # if( 400 <= word["x0"] <= 550 and 0<= word["top"] <= 60):
        #     print(word["text"] , word["x0"], word["top"])
        #print("8")
        #print(word["text"], box["x_min"],word["x0"])
        #to debug
        # if word["text"] == "03/02/2026":
        #     print("FOUND DATE")
        #     print(word)

        #     print(
        #         box["x_min"] <= word["x0"] <= box["x_max"],
        #         box["y_min"] <= word["top"] <= box["y_max"]
        #     )
        
        # if word["text"] == "124503":
        #     print("FOUND 124503")
        #     print("x0 =", word["x0"])
        #     print("top =", word["top"])

        #     print(
        #         box["x_min"] <= word["x0"] <= box["x_max"],
        #         box["y_min"] <= word["top"] <= box["y_max"]
        #     )
        if(box["x_min"] <= word["x0"] <= box["x_max"] and box["y_min"] <= word["top"] <= box["y_max"]):
            selected.append(word)
        #print("SELECTED: ", selected)
    selected.sort(key=lambda x: x["x0"])
        
    return " ".join(w["text"] for w in selected)
    
# grouping them into rows
def group_rows(words,tolerance = 8 ):
    rows = []
    words = sorted(words, key = lambda x: (x["page"],x["top"]))
    for word in words :

        if not rows:
            rows.append([word])
            continue

        last_row = rows[-1]
        avg_y = sum(w["top"] for w in last_row) / len(last_row)
        last_page = last_row[0]["page"]

        if (word["page"] == last_page and abs(word["top"] - avg_y) <= tolerance ) :
            last_row.append(word)
        else:
            rows.append([word])
        # print(word["top"], word["text"])
        # y = round(word["top"]/tolerance)*tolerance
        # rows.setdefault(y, []).append(word)
    #adding debugging
    # for y,row in sorted(rows.items()):
    #     print(
    #         y,
    #         [w["text"] for w in sorted(row,key = lambda x:x["x0"])]
    #     )
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
    #debugging : 
    # print("Rows Found: ", len(rows))
    # for y,row in sorted(rows.items()):
    #     print(y, len(row))
    
    # print(type(rows))

    # for k, v in rows.items():
    #     print("KEY TYPE:", type(k))
    #     print("VALUE TYPE:", type(v))
    #     print(v[:2])
    #     break

    products = []

    for row in rows:
        product = {
            'part_number' : " ",
            'description' : " ",
            "quantity" : " ",
            "price" : " ",
            "net" : " ",
            "line_total" : " "
        }
        # for row in rows.values():
        #     print("ROW TYPE:", type(row))
        #     if len(row):
        #         print("first element type =", type(row[0]))
        #     break
        #     print("FIRST:", row[:2])
        #     break
        row = sorted(row, key = lambda x:x["x0"])
        # print(type(rows))


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
        if (product["description"] != "" or product["part_number"] != "" or product["quantity"] != "" or product["price"]!= ""):
            for k in product:
                product[k] = product[k].strip()
            
            part = product["part_number"]
            

            if not any(ch.isdigit() for ch in part):
                continue
            if "/" in part:
                continue
            products.append(product)
    return products



def group_by_page(words):

    pages = {}

    for word in words:
        page_no = word["page"]

        if page_no not in pages:
            pages[page_no] = []

        pages[page_no].append(word)

    return pages

def extract_napa_feilds(coord_path):
    words = load_coordinates(coord_path)
    # debug
    # found = False
    # for word in words:
    #     if word["text"] == "124503":
    #         found = True
    #         print("Found 124503 : ")
    #         print(word)
    # print("FOUND?" , found)
    result = {}
    pages = group_by_page(words)
    all_invoices = []
    # print("TYPE OF WORDS:", type(words))
    # print("FIRST ITEM TYPE:", type(words[0]))
    # print("FIRST ITEM:", words[0])

    #print("result")
    for page_no , page_words in pages.items():
        invoice = {}
        
        invoice["invoice_number"] = words_in_box(
            page_words,
            TEMPLATE["invoice_number"]
        )
        import re 
        match = re.search(r'\b\d{6}\b', invoice["invoice_number"])
        if match : 
            invoice["invoice_number"] = match.group()

        invoice["invoice_date"] = words_in_box(
            page_words,
            TEMPLATE["invoice_date"]
        )
        
        match = re.search(
            r'\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}',
            invoice["invoice_date"]
        )

        if match:
            invoice["invoice_date"] = match.group()

        invoice["po_number"] = words_in_box(
            page_words,
            TEMPLATE["po_number"]
        )
        match = re.search(r'R\d+', invoice["po_number"])
        if match:
            invoice["po_number"] = match.group()

        invoice["subtotal"] = words_in_box(
            page_words,
            TEMPLATE["subtotal"]
        )

        match = re.search(r'-?\d+\.\d{2}', invoice["subtotal"])
        if match:
            invoice["subtotal"] = match.group()

        invoice["tax"] = words_in_box(
            page_words,
            TEMPLATE["tax"]
        )
        numbers = re.findall(r'-?\d+\.\d{2}', invoice["tax"])
        if numbers:
            invoice["tax"] = numbers[-1]

        invoice["total"] = words_in_box(
            page_words,
            TEMPLATE["invoice_total"]
        )
        match = re.search(r'-?\d+\.\d{2}', invoice["total"])
        if match:
            invoice["total"] = match.group()


        invoice["products"] = extract_products(page_words)

        all_invoices.append(invoice)

    return all_invoices

    # result["invoice_number"] = words_in_box( page_words , TEMPLATE["invoice_number"])
    # result["invoice_date"] = words_in_box( words , TEMPLATE["invoice_date"])
    # result["po_number"] = words_in_box( words , TEMPLATE["po_number"])
    # result["subtotal"] = words_in_box( words , TEMPLATE["subtotal"])
    # result["tax"] = words_in_box( words , TEMPLATE["tax"])
    # result["total"] = words_in_box( words , TEMPLATE["invoice_total"])
    # result["products"] = extract_products(words)
    # return result