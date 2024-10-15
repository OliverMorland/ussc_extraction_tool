import fitz  # PyMuPDF
import re


def extract_and_split_text(pdf_path, split_string):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    full_text = ""

    # Extract text from each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        full_text += page.get_text()

    # Split the text based on the specified string
    chunks = full_text.split(split_string)
    return chunks


def extract_and_split_text_by_numbered_list(full_text):
    # Regular expression to match numbered list items (e.g., 1., 2., 3., etc.)
    pattern = re.compile(r'\n\d+\.\s')

    # Split the text based on the numbered list items
    chunks = pattern.split(full_text)

    # Remove any leading empty chunk
    if chunks[0] == '':
        chunks = chunks[1:]

    return chunks


def remove_items_without_date_from_list(items):
    global i
    for i in range(len(items) - 1, -1, -1):
        if not re.search(r'\d{2}/\d{2}/\d{4}', items[i]):
            items.pop(i)


def get_charges_from_sample_pdf(pdf_path):
    split_string = "Date Sentence\nImposed/Disposition\nGuideline\nPoints"
    chunks = extract_and_split_text(pdf_path, split_string)

    charges = []
    for i in range(1, len(chunks)):
        # Extract the charge information
        numbered_items = extract_and_split_text_by_numbered_list(chunks[i])
        for item in numbered_items:
            charges.append(item)

    remove_items_without_date_from_list(charges)
    return charges
