import re

import fitz  # PyMuPDF
import os


def extract_text(pdf_path, output_dir):
    """Extracts text from each page of the PDF and saves it to a text file."""
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        pdfData = extract_information(text)
        print("PDF Data:")
        for key, value in pdfData.items():
            print(f"{key} ==> {value}")
        with open(os.path.join(output_dir, f"page_{page_num + 1}.txt"), "w", encoding="utf-8") as f:
            f.write(text)


def extract_images(pdf_path, output_dir):
    """Extracts images from the PDF and saves them as separate files."""
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = os.path.join(output_dir, f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}")
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)


def extract_metadata(pdf_path):
    """Extracts metadata from the PDF."""
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    return metadata

def extract_information(text):
    phone_numbers = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    names = re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', text)  # Simplistic name extraction
    invoice_numbers = re.findall(r'\bInvoice\s*#?\s*\d+\b', text)
    item_details = re.findall(r'\bItem\s*#?\s*\d+\b.*?\bPrice\s*\$\d+\.\d{2}\b', text, re.DOTALL)

    patterns = {
       # 'Name': r'Επωνυμία\s*:\s*(.+)',
       # 'Profession': r'Επάγγελμα\s*:\s*(.+)',
        'VAT number': r'Α.Φ.Μ. - Δ.Ο.Υ.:\s*(.+)',
        'Tax Office': r'Δ.Ο.Υ.\s*:\s*(.+)',
       # 'Address': r'Διεύθυνση\s*-\s*Πόλη\s*:\s*(.+)',
       # 'City': r'Διεύθυνση\s*-\s*Πόλη\s*:\s*.+\s*-\s*(.+)',
        #'P.C. - Chora': r'Τ\.Κ\.\s*-\s*Χώρα\s*:\s*(.+)',
        'Purpose of Transport': r'Σκοπός\nΔιακίνησης\s*:\s*(.+)',
        'Place of Loading': r'Τόπος Φόρτωσης\s*:\s*(.+)',
        #'Shipping Method': r'Τρόπος\nΑποστολής\s*:\s*(.+)',
        #'Place of Destination': r'Τόπος\nΠροορισμού\s*:\s*(.+)',
        #'Telephone': r'ΤΗΛΕΦΩΝΟ\.\s*:\s*(.+)',
        #'G.E.MI. Number': r'Αριθμός Γ\.Ε\.ΜΗ\s*:\s*(\d+)',
        'Type of document': r'Είδος Παραστατικού\s*:\s*(.+)',
        'Date': r'Ημερομηνία\s*:\s*(\d{2}/\d{2}/\d{4})',
        'Row': r'Σειρά\s*:\s*(.+)',
        'Payment terms': r'Όροι Πληρωμής\s*:\s*(.+)',
        'Hour': r'Ώρα\s*:\s*(.+)',
        'COLLECTION': r'ΠΑΡΑΛΑΒΗ\s*:\s*(.+)',
        'VERSION': r'ΕΚΔΟΣΗ\s*:\s*(.+)',
        'Bank Accounts': r'Tραπεζικοί Λογαριασμοί\s*:\s*(.+)',
        #'reference for your payment': r'αναφορά για την πληρωμή σας\s*:\s*(.+)',
        #'Comments': r'Παρατηρήσεις:\s*(.+)',
        #'Current Balance': r'Τρέχον Υπόλοιπο\s*(.+) €',
        #'Amount before deduction': r'Ποσό Προ Έκπτωσης\s*(.+) €',
        #'Discount': r'Έκπτωση\s*(.+) €',
        #'Net Worth': r'Καθαρή Αξία\s*(.+) €',
        #'Vat 24%': r'ΦΠΑ 24,00%\s*(.+) €',
        #'Total': r'Σύνολο\s*(.+) €',
        'DESCRIPTION': r'ΠΕΡΙΓΡΑΦΗ\s*:\s*(.+)',
        'QUANTITY': r'ΠΟΣΟΤΗΤΑ\s*:\s*(.+)',
        'Unit Price': r'ΤΙΜΗ ΜΟΝΑΔΑΣ\s*:\s*(.+)',
        'Value': r'ΑΞΙΑ\s*:\s*(.+)',
    }

    extracted_data = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        extracted_data[key] = match.group(1) if match else None

    extracted_data['emails'] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

    return extracted_data


def main(pdf_path, output_dir):
    """Main function to extract text, images, and metadata from the PDF."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Extracting text...")
    extract_text(pdf_path, output_dir)
    print("Text extraction completed.")

    print("Extracting images...")
    extract_images(pdf_path, output_dir)
    print("Image extraction completed.")

    print("Extracting metadata...")
    metadata = extract_metadata(pdf_path)
    print("Metadata extraction completed.")
    print("PDF Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    pdf_path = "Invoice__24-0588.pdf"  # Replace with your PDF file path
    output_dir = "output"  # Replace with your desired output directory
    main(pdf_path, output_dir)
