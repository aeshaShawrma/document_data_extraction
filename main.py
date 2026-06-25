import pdfplumber

pdf_path= r"data\invoices\invoices\Upload2.pdf"
with pdfplumber.open(r"C:\Users\Aesha.sharma\document_extraction\data\invoices\invoices\Upload2.pdf") as pdf:
    text =""

    for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text+=page_text +"\n"
  
print(text[:3000])

prompt = f'''
    You are an invoice data extraction system.
    Extract only values explicitly present int the document.property
    Do not calculate. 
    do not infer.
    do not estimate.
    Return valid JSON only.property
    Document:
   '''
