import pandas as pd
from fpdf import FPDF
import json
from PIL import Image, ImageDraw
import os

# Load the CSV file
file_path = 'invoices.csv'
invoices_df = pd.read_csv(file_path)

# Create a placeholder image (100x50 pixels) for the logo
placeholder_logo_path = 'invoices/selfmade-black.jpg'
placeholder_logo = Image.new('RGB', (100, 50), color='gray')
draw = ImageDraw.Draw(placeholder_logo)
draw.text((10, 20), 'Logo', fill='black')
placeholder_logo.save(placeholder_logo_path)

# Define the path to the TTF font file (make sure to upload this font file)
ttf_font_path = 'fonts/DejaVuSans.ttf'


class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, 'Advocate Mohit Rajendra Balani', 0, 1, 'L')
        self.set_font('DejaVu', 'I', 12)
        self.cell(0, 10, 'B.com A.C.A LLB Advocate', 0, 1, 'L')
        self.cell(0, 10, '833 Gala Empire, Opp. Doordarshan TV Tower,', 0, 1, 'L')
        self.cell(0, 10, 'Drive-in road, Ahmedabad-380052', 0, 1, 'L')
        self.cell(0, 10, 'Phone: +91 8238036174', 0, 1, 'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_invoice_body(self, data):
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, 'MEMO OF FEES', 0, 1, 'R')
        self.ln(10)

        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 10, f'MOF # {data["number"]}', 0, 1, 'R')
        self.cell(0, 10, f'Date: {data["date"]}', 0, 1, 'R')
        self.ln(10)

        self.set_font('DejaVu', '', 12)
        self.cell(0, 10, 'To,', 0, 1, 'L')
        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 10, data["to_who"], 0, 1, 'L')
        self.ln(10)

        # Invoice Items
        items = json.loads(data["items"])
        self.set_font('DejaVu', 'B', 12)
        self.cell(15, 10, 'Sr. No.', 1)
        self.cell(115, 10, 'DESCRIPTION', 1)
        self.cell(30, 10, 'Fees', 1)
        self.cell(30, 10, 'TOTAL', 1)
        self.ln()

        self.set_font('DejaVu', '', 12)
        for idx, item in enumerate(items, 1):
            self.cell(15, 10, str(idx), 1)
            self.cell(115, 10, item['name'], 1)
            self.cell(30, 10, f"₹{item['unit_cost']}", 1, 0, 'R')
            self.cell(30, 10, f"₹{item['quantity'] * item['unit_cost']}", 1, 0, 'R')
            self.ln()

        self.ln(10)
        self.set_font('DejaVu', 'B', 12)
        self.cell(160, 10, 'SUBTOTAL', 1)
        self.set_font('DejaVu', '', 12)
        subtotal = sum(item['quantity'] * item['unit_cost'] for item in items)
        self.cell(30, 10, f"₹{subtotal}", 1, 1, 'R')

        self.set_font('DejaVu', 'B', 12)
        self.cell(160, 10, 'TOTAL due', 1)
        self.set_font('DejaVu', '', 12)
        self.cell(30, 10, f"₹{subtotal}", 1, 1, 'R')

        self.ln(10)
        self.cell(0, 10, 'Please make cheque in favor of Mohit Rajendra Balani', 0, 1, 'L')
        self.cell(0, 10, 'Bank A/c Details:', 0, 1, 'L')
        self.cell(0, 10, 'A/c Name : Mohit Rajendra Balani', 0, 1, 'L')
        self.cell(0, 10, 'Axis Bank Chandlodiya Branch Ahmedabad', 0, 1, 'L')
        self.cell(0, 10, 'A/c No.: 916010009266800', 0, 1, 'L')
        self.cell(0, 10, 'IFSC: UTIB0000728', 0, 1, 'L')
        self.ln(10)
        self.cell(0, 10, 'If you have any questions concerning this invoice contact @ cases@mohitbalani.com', 0, 1, 'L')
        self.cell(0, 10, 'PAN No. BLAPB0566L', 0, 1, 'L')
        self.ln(20)
        self.cell(0, 10, 'Mohit Rajendra Balani', 0, 1, 'R')
        self.cell(0, 10, 'Advocate', 0, 1, 'R')


def generate_invoice(data):
    pdf = PDF()
    pdf.add_font('DejaVu', '', ttf_font_path, uni=True)
    pdf.add_font('DejaVu', 'B', ttf_font_path, uni=True)
    pdf.add_font('DejaVu', 'I', ttf_font_path, uni=True)
    pdf.add_page()
    pdf.add_invoice_body(data)

    output_filename = f'invoices/Invoice_{data["number"]}.pdf'
    pdf.output(output_filename)
    return output_filename


# Generate invoices for each row in the dataframe
invoice_files = []
for index, row in invoices_df.iterrows():
    invoice_data = row.to_dict()
    invoice_file = generate_invoice(invoice_data)
    invoice_files.append(invoice_file)

print(invoice_files)
