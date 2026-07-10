from vendor_detector import detect_vendor
from invoice_detector import get_invoice_number


def build_invoice_groups(pages):

    groups = {}

    for page_no, words in pages.items():

        page_text = " ".join(
            w["text"]
            for w in words
        )

        vendor = detect_vendor(page_text)

        invoice_number = get_invoice_number(
            page_text
        )

        key = (
            vendor,
            invoice_number
        )

        if key not in groups:

            groups[key] = {
                "vendor": vendor,
                "invoice_number": invoice_number,
                "pages": []
            }

        groups[key]["pages"].append(page_no)

    return list(groups.values())
