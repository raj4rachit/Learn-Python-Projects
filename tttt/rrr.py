import re


def extract_data(text):
    # Extract the Invoice information
    invoice_info = re.search(r'Ώρα\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n', text)
    invoice_details = ''
    if invoice_info:
        invoice_details = {
            'Document Type': invoice_info.group(1),
            'Series': invoice_info.group(2),
            'Date': invoice_info.group(3),
            'Payment Terms': invoice_info.group(4),
            'Time': invoice_info.group(5),
        }

    # Extract the Description, Quantity, Unit Price, and Total
    description_info = re.search(r'\[SKU : (.+?)\] (.+?) - per 100 GB\n(.+?)\n(.+?)\n \nUnits\n(.+?)\n(.+?)%\n(.+?)\n',
                                 text)
    description_details = ''
    if description_info:
        description_details = {
            'SKU': description_info.group(1),
            'Description': description_info.group(2),
            'Service': description_info.group(3),
            'Quantity': description_info.group(4),
            'Unit Price': description_info.group(5),
            'Tax Rate': description_info.group(6),
            'Total': description_info.group(7),
        }

    # Extract the Payment Reference
    payment_reference = re.search(r'Χρησιμοποιήστε την ακόλουθη αναφορά για την πληρωμή σας: \n(.+?)\n', text).group(1)

    # Extract the Bank Accounts
    bank_accounts = re.findall(r'IBAN: (.+)', text)
    banks = ['Alpha Bank', 'Πειραιώς', 'Eurobank', 'Revolut']
    bank_details = dict(zip(banks, bank_accounts))

    # Extract the Beneficiary
    beneficiary = re.search(r'Beneficiary: (.+)', text).group(1)

    # Extract the Customer Information
    #customer_info = re.search(r'Στοιχεία Συναλλασσόμενου\nΕπωνυμία\n:\n(.+?)\nΕπάγγελμα\n:\n(.+?)\nΑ.Φ.Μ. - Δ.Ο.Υ.\n:\n(.+?)\n -\n(.+?)\nΔιεύθυνση - Πόλη\n:\n(.+?)\n - \n(.+?)\nΤ.Κ. - Χώρα\n:\n(.+?)\n - \n(.+?)\n',text)
    customer_info = re.search(
        r'Στοιχεία Συναλλασσόμενου\nΕπωνυμία\n:\n(.+?)\nΕπάγγελμα\n:\n(.+?)\n',
        text)
    customer_details=''
    if customer_info:
        customer_details = {
            'Name': customer_info.group(1),
            'Occupation': customer_info.group(2),
            'VAT number': re.search(r'Α.Φ.Μ. - Δ.Ο.Υ.\n:\n(.+?)\n', text).group(1),
            'Address': re.search(r'Διεύθυνση - Πόλη\n:\n(.+?)\n - \n(.+?)\n', text).group(1)+ ' - ' +re.search(r'Διεύθυνση - Πόλη\n:\n(.+?)\n - \n(.+?)\n', text).group(2),
            'City': re.search(r'Διεύθυνση - Πόλη\n:\n(.+?)\n - \n(.+?)\n', text).group(2),
            'Postal Code': re.search(r'Τ.Κ. - Χώρα\n:\n(.+?)\n - \n(.+?)\n', text).group(1),
            'Country': re.search(r'Τ.Κ. - Χώρα\n:\n(.+?)\n - \n(.+?)\n', text).group(2),
        }

    # Extract the Total Balance
    total_balance = re.search(r'Τρέχον Υπόλοιπο\n(.+?)\n', text).group(1)

    # Extract the Transaction Details
    transaction_details = re.search(
        r'Ποσό Προ Έκπτωσης\n(.+?)\nΈκπτωση\n(.+?)\nΚαθαρή Αξία\n(.+?)\nΦΠΑ (.+?)%\n(.+?)\nΣύνολο\n(.+?)\n', text)
    transaction_summary=''
    if transaction_details:
        transaction_summary = {
            'Pre-discount Amount': transaction_details.group(1),
            'Discount': transaction_details.group(2),
            'Net Value': transaction_details.group(3),
            'VAT Rate': transaction_details.group(4),
            'VAT Amount': transaction_details.group(5),
            'Total Amount': transaction_details.group(6),
        }

    # Collect all extracted data
    extracted_data = {
        'Invoice Details': invoice_details,
        'Description Details': description_details,
        'Payment Reference': payment_reference,
        'Bank Details': bank_details,
        'Beneficiary': beneficiary,
        'Customer Details': customer_details,
        'Total Balance': total_balance,
        'Transaction Summary': transaction_summary,
    }

    return extracted_data


text = """Είδος Παραστατικού\nΣειρά\nΗμερομηνία\nΌροι Πληρωμής\nΏρα\nΤιμολόγιο Παροχής Υπηρεσιών\nΤΠΥ 24-0588\n02/05/2024\nΠίστωση 15 Ημερών\n00:00\nΠΕΡΙΓΡΑΦΗ\nΠΟΣΟΤΗΤΑ\nΤΙΜΗ ΜΟΝΑΔΑΣ\nΦΟΡΟΙ\nΑΞΙΑ\nΑπρίλιος 2024\nPer gigabyte\n[SKU : SPBAMSENS] Acronis CPC Cloud Storage - per 100 GB\nAcronis Cyber Protect Cloud Storage, SKU : SPBAMSENS\n4,00\n \nUnits\n11,00\n24,00%\n44,00\n €\nΧρησιμοποιήστε την ακόλουθη αναφορά για την πληρωμή σας: \nΤΠΥ 24-0588\nΤραπεζικοί Λογαριασμοί\n \nBeneficiary: TicTac Ltd\n \nΕΚΔΟΣΗ\n \nΠΑΡΑΛΑΒΗ\n \nAlpha Bank IBAN: GR6401401540154002320016144\n \nΠειραιώς IBAN: GR4201721210005121084907511\n \nEurobank IBAN: GR7902604320000220200243111\n \nRevolut IBAN: LT86 3250 0407 1677 4102\n \nTerms & Conditions: https://crm.tictac.gr/terms\nΣτοιχεία Συναλλασσόμενου\nΕπωνυμία\n:\nHELPVISOR IKE\nΕπάγγελμα\n:\nIT Provider\nΑ.Φ.Μ. - Δ.Ο.Υ.\n:\n800822009\n -\nΔιεύθυνση - Πόλη\n:\nΠΑΝΙΔΗ 31\n - \nΧΑΛΚΙΔΑ\nΤ.Κ. - Χώρα\n:\n34100\n - \nΕΛΛΑΔΑ\nΣτοιχεία Παράδοσης\nΣκοπός\nΔιακίνησης\n:\nΤόπος Φόρτωσης\n:\nΤρόπος\nΑποστολής\n:\n-\nΤόπος\nΠροορισμού\n:\n- \nΧΑΛΚΙΔΑ\nΤρέχον Υπόλοιπο\n632,40\n €\nΠαρατηρήσεις:\nTerms & Conditions: https://crm.tictac.gr/terms\nΠοσό Προ Έκπτωσης\n44,00\n €\nΈκπτωση\n0,00\n €\nΚαθαρή Αξία\n44,00 €\nΦΠΑ 24,00%\n10,56 €\nΣύνολο\n54,56 €\nwww.tictac.gr - www.tictaclabs.com\nΤΙΚΤΑΚ ΙΚΕ\n \nDATA RECOVERY AND CYBER SECURITY\n \nΑΦΜ: EL800782394, ΔΟΥ: ΗΛΙΟΥΠΟΛΗΣ\n \nΤΡΙΠΟΛΕΩΣ 9, 172 37, ΥΜΗΤΤΟΣ\n \nΤΗΛΕΦΩΝΟ.: 210 6897383\nΑριθμός Γ.Ε.ΜΗ: 140756708000\ninfo@tictac.gr - info@tictaclabs.com\nPage: \n1\n / \n2MARK: - UID:\nwww.tictac.gr - www.tictaclabs.com\nΤΙΚΤΑΚ ΙΚΕ\n \nDATA RECOVERY AND CYBER SECURITY\n \nΑΦΜ: EL800782394, ΔΟΥ: ΗΛΙΟΥΠΟΛΗΣ\n \nΤΡΙΠΟΛΕΩΣ 9, 172 37, ΥΜΗΤΤΟΣ\n \nΤΗΛΕΦΩΝΟ.: 210 6897383\nΑριθμός Γ.Ε.ΜΗ: 140756708000\ninfo@tictac.gr - info@tictaclabs.com\nPage: \n2\n / \n2"""

extracted_data = extract_data(text)
for key, value in extracted_data.items():
    print(f"{key}: {value}")
