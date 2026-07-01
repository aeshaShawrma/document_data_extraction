import json

with open("coordinates_Napa/Napa1.json") as f :
    words = json.load(f)

for word in words:
    print(
        word["text"] ,
        "x = " , round(word["x0"]),
        "y = " , round(word["top"])
    )