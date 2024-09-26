import pandas as pd
from fpdf import FPDF
import os

# Load the CSV file
file_path = 'invoicessingle.csv'
invoices_df = pd.read_csv(file_path)
image_path = 'sign.png'  # Define the path to the image file

# Define the path to the TTF font file (make sure to upload this font file)
ttf_font_path = 'fonts/DejaVuSans.ttf'
ttf_font_path1 = 'fonts/C059-Bold.ttf'
ttf_font_path2 = 'fonts/DejaVuSans-Bold.ttf'


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_invoice_body(self, data):
        self.set_font('Century Schoolbook Std', 'B', 14)
        self.cell(0, 10, 'Advocate Mohit Rajendra Balani', 0, 1, 'C')

        self.set_font('Century Schoolbook Std', 'B', 14)
        self.cell(0, 6, 'B.com, A.C.A, LLB, Advocate', 0, 1, 'C')

        x = self.get_x()
        y = self.get_y()

        # Draw a line below the text
        self.line(10, y + 1, 200, y + 1)
        self.ln(4)
        self.set_font('DejaVu', '', 12)
        self.cell(0, 6, '833, Gala Empire, Opp. Doordarshan TV Tower,', 0, 1, 'C')
        self.cell(0, 6, 'Drive-in road, Ahmedabad-380052', 0, 1, 'C')
        self.cell(0, 6, 'Phone: +91 8238036174', 0, 1, 'C')
        self.ln(10)

        self.set_font('Century Schoolbook Std', 'B', 14)
        self.cell(0, 10, 'MEMO OF FEES', 0, 1, 'C')
        self.set_font('Century Schoolbook Std', 'B', 12)
        self.cell(120, 6, f'MOF # {data["mof"]}', 0, 0, 'L')
        self.cell(0, 6, f'DATE: {data["date"]}', 0, 1, 'R')
        self.ln(10)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 6, 'To,', 0, 1, 'L')
        self.set_font('DejaVu', '', 12)
        self.cell(0, 6, data["to_who"], 0, 1, 'L')
        self.set_font('DejaVu', '', 8)
        self.cell(0, 6, 'C/o', 0, 1, 'L')
        self.set_font('DejaVu', '', 12)
        self.cell(0, 6, data["co"], 0, 1, 'L')
        self.ln(10)

        # Invoice Items
        self.set_font('DejaVu', '', 12)
        self.cell(15, 10, 'Sr. No', 1)
        self.cell(105, 10, 'DESCRIPTION', 1)
        self.cell(35, 10, 'Fees', 1)
        self.cell(35, 10, 'TOTAL', 1)
        self.ln()
        # Wrap text in the DESCRIPTION cell
        description = data['legal_description']
        max_width = 105
        line_height = self.font_size * 1.5

        # Split the description into multiple lines
        desc_lines = self.multi_cell(max_width, line_height, description, border=0, align='L', split_only=True)
        dsl=len(desc_lines)
        cell_height = max(len(desc_lines) * line_height, 10)

        if dsl > 1:
            self.set_font('DejaVu', '', 12)
            # self.cell(15, 10, str(1), 1)
            self.set_xy(self.get_x(), self.get_y())
            self.cell(15, cell_height, str(1), 1)
            self.set_xy(self.get_x(), self.get_y() + cell_height)

            # Set the cursor position for the next cell
            self.set_xy(self.get_x(), self.get_y() - cell_height)

            # Create the multi-cell for the description
            self.multi_cell(105, line_height, description, border=1, align='L')

            # Move the cursor position to the next cell
            x_after_description = self.get_x()
            y_after_description = self.get_y()

            # Draw the Fees cell
            self.set_xy(x_after_description + 120, y_after_description - cell_height)
            self.cell(35, cell_height, f"₹{data['fees']}", 1, 0, 'R')

            # Draw the TOTAL cell
            self.cell(35, cell_height, f"₹{data['fees'] * 1}", 1, 0, 'R')
            self.ln(cell_height)
        else:
            self.set_font('DejaVu', '', 12)
            self.cell(15, 10, str(1), 1)
            self.cell(105, 10, description, 1)
            self.cell(35, 10, f"₹{data['fees']}", 1, 0, 'R')
            self.cell(35, 10, f"₹{data['fees'] * 1}", 1, 0, 'R')
            self.ln()


        self.set_font('DejaVu', '', 12)
        self.cell(155, 10, 'SUBTOTAL', 1, 0, 'R')
        self.set_font('DejaVu', '', 12)
        subtotal = data['fees']
        self.cell(35, 10, f"₹{subtotal}", 1, 0, 'R')
        self.ln()

        self.set_font('DejaVu', '', 12)
        self.cell(155, 10, 'TOTAL DUE', 1)
        self.set_font('DejaVu', 'B', 12)
        self.cell(35, 10, f"₹{subtotal}", 1, 0, 'R')
        self.ln(20)

        self.set_font('DejaVu', '', 12)
        self.cell(0, 6, 'Please make cheque in favor of Mohit Rajendra Balani', 0, 1, 'L')
        self.cell(0, 6, 'Bank A/c Details', 0, 1, 'L')
        self.cell(0, 6, 'A/c Name: Mohit Rajendra Balani', 0, 1, 'L')
        self.cell(0, 6, 'Axis Bank, Chandlodiya Branch, Ahmedabad', 0, 1, 'L')
        self.cell(0, 6, 'A/c No.: 916010009266800', 0, 1, 'L')
        self.cell(0, 6, 'IFSC: UTIB0000728', 0, 1, 'L')
        self.ln(10)
        self.cell(130, 6, 'If you have any questions concerning this invoice, contact @ ', 0, 0, 'L')
        self.set_text_color(0, 0, 255)
        self.cell(0, 6, 'Mrbalanibilling@gmail.com', 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.set_font('DejaVu', '', 12)
        self.cell(18, 6, 'PAN No. ', 0, 0, 'L')
        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 6, 'BLAPB0566L', 0, 1, 'L')
        self.ln(20)
        self.add_image(image_path)
        self.cell(0, 6, 'Mohit Rajendra Balani', 0, 1, 'R')
        self.cell(0, 6, 'Advocate', 0, 1, 'R')

    def add_image(self, image_path):
        x_after_description = self.get_x()
        y_after_description = self.get_y()
        self.image(image_path, x=self.get_x()+150, y=self.get_y()-25, w=30)


def generate_invoice(data):
    pdf = PDF()
    pdf.add_font('DejaVu', '', ttf_font_path, uni=True)
    pdf.add_font('DejaVu', 'B', ttf_font_path2, uni=True)
    pdf.add_font('DejaVu', 'I', ttf_font_path, uni=True)
    pdf.add_font('Century Schoolbook Std', 'B', ttf_font_path1, uni=True)
    pdf.add_page()
    pdf.add_invoice_body(data)
    output_filename = f'invoices/{data["mof"]}_{data["to_who"]}.pdf'
    pdf.output(output_filename)
    return output_filename


# Generate invoices for each row in the dataframe
invoice_files = []
for index, row in invoices_df.iterrows():
    invoice_data = row.to_dict()
    invoice_file = generate_invoice(invoice_data)
    invoice_files.append(invoice_file)

print(invoice_files)
