import fitz
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import PyPDF2
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

def extract_text(pdf_path, output_dir):
    """Extracts text from each page of the PDF and saves it to a text file."""
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
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

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


def readPDF(file_path):
    pdf_text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text() if page.extract_text() else ""
    return pdf_text


def extract_information(text):
    phone_numbers = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    names = re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', text)  # Simplistic name extraction
    invoice_numbers = re.findall(r'\bInvoice\s*#?\s*\d+\b', text)
    item_details = re.findall(r'\bItem\s*#?\s*\d+\b.*?\bPrice\s*\$\d+\.\d{2}\b', text, re.DOTALL)

    patterns = {
        'Name': r'Επωνυμία\s*:\s*(.+)',
        'Profession': r'Επάγγελμα\s*:\s*(.+)',
        'VAT number': r'Α\.Φ\.Μ\.\s*:\s*(\d+)',
        'Tax Office': r'Δ\.Ο\.Υ\.\s*:\s*(.+)',
        'Address': r'Διεύθυνση\s*-\s*Πόλη\s*:\s*(.+)',
        'City': r'Διεύθυνση\s*-\s*Πόλη\s*:\s*.+\s*-\s*(.+)',
        'P.C. - Chora': r'Τ\.Κ\.\s*-\s*Χώρα\s*:\s*(.+)',
        'Purpose of Transport': r'Σκοπός Διακίνησης\s*:\s*(.+)',
        'Place of Loading': r'Τόπος Φόρτωσης\s*:\s*(.+)',
        'Shipping Method': r'Τρόπος Αποστολής\s*:\s*(.+)',
        'Place of Destination': r'Τόπος Προορισμού\s*:\s*(.+)',
        'Telephone': r'ΤΗΛΕΦΩΝΟ\.\s*:\s*(.+)',
        'G.E.MI. Number': r'Αριθμός Γ\.Ε\.ΜΗ\s*:\s*(\d+)',
        'Type of document': r'Είδος Παραστατικού\s*:\s*(.+)',
        'Date': r'Ημερομηνία\s*:\s*(\d{2}/\d{2}/\d{4})',
        'Row': r'Σειρά\s*:\s*(.+)',
        'Payment terms': r'Όροι Πληρωμής\s*:\s*(.+)',
        'Hour': r'Ώρα\s*:\s*(.+)',
        'COLLECTION': r'ΠΑΡΑΛΑΒΗ\s*:\s*(.+)',
        'VERSION': r'ΕΚΔΟΣΗ\s*:\s*(.+)',
        'Bank Accounts': r'Tραπεζικοί Λογαριασμοί\s*:\s*(.+)',
        'reference for your payment': r'αναφορά για την πληρωμή σας\s*:\s*(.+)',
        'Comments': r'Παρατηρήσεις:\s*(.+)',
        'Current Balance': r'Τρέχον Υπόλοιπο\s*(.+) €',
        'Amount before deduction': r'Ποσό Προ Έκπτωσης\s*(.+) €',
        'Discount': r'Έκπτωση\s*(.+) €',
        'Net Worth': r'Καθαρή Αξία\s*(.+) €',
        'Total': r'Σύνολο\s*(.+) €',
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
    # return {
    #     'phone_numbers': phone_numbers,
    #     'emails': emails,
    #     'names': names,
    #     'invoice_numbers': invoice_numbers,
    #     'item_details': item_details
    # }


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        flash('No file part')
        return redirect(request.url)

    files = request.files.getlist('files')
    uploaded_files = []
    pdf_texts = []
    extracted_data = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files.append(filename)
            pdf_text = readPDF(file_path)
            pdf_texts.append(pdf_text)
            extract_text(file_path,'uploads')
            extracted_data.append(extract_information(pdf_text))

    context_data = []
    for index, text in enumerate(pdf_texts):
        context_data.append({
            'index': index,
            'pdf_text': pdf_texts,
            'extracted_data': extracted_data[index]
        })

    if not uploaded_files:
        flash('No files uploaded. Please check the file types.')
    else:
        flash('Files successfully uploaded')

    return render_template('results.html', uploaded_files=uploaded_files, context_data=context_data)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.secret_key = 'supersecretkey'
    app.run(debug=True)
