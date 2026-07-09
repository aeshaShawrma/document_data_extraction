
import re

def get_invoice_number(text):

    patterns = [

        r'\b\d{4}-\d{5,}\b',      # O'Reilly

        r"\b\d{2}IV\d{6}\b",           # Auto Parts Warehouse

        r"\b20\d{11}\b" ,          # Advance Auto

        r'\b\d{11}\b',       #autozone

        r"(\d{10,20})" ,     #carquest

        r'\b\d{6}\b',       #napa

        r"\b\d{8}\b" ,      #worldpac

        
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group()

    return None
