def normalize(invoice, vendor):

    return {

        "vendor_name": vendor,

        "invoice_number":
            invoice.get("invoice_number",""),

        "invoice_date":
            invoice.get("invoice_date",""),

        "po_number":
            invoice.get("po_number",""),

        "subtotal":
            invoice.get("subtotal",""),

        "tax":
            invoice.get("tax",""),

        "invoice_total":
            invoice.get("invoice_total",""),

        "products":
            invoice.get("products",[])
    }
