import csv
import fitz  # PyMuPDF
import re
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch

# Load the fine-tuned model
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-distilled-squad')


# Function to extract and split text from the PDF
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


# Define the data to be written to the CSV file
data = [
    {
        'Arrest Date': '2023-01-01',
        'J/A': 'J',
        'Sentence Date': '2023-02-01',
        'Custody Length Imposed': '24 months',
        'Custody Length From': '2023-02-01',
        'Custody Length To': '2025-02-01',
        'Probation Length': '12 months',
        'Guideline': 'Guideline 1',
        'Points': 5,
        'State': 'CA',
        'Federal': 'Yes',
        'Tribal': 'No',
        'Offenses': 'Offense 1'
    },
    # Add more rows as needed
]

# Define the CSV file name
csv_file = 'output.csv'

# Define the column names
columns = [
    'Arrest Date', 'J/A', 'Sentence Date', 'Custody Length Imposed', 'Custody Length From',
    'Custody Length To', 'Probation Length', 'Guideline', 'Points', 'State', 'Federal',
    'Tribal', 'Offenses'
]


# Function to add a row to the data
def add_row(arrest_date, ja, sentence_date, custody_length_imposed, custody_length_from, custody_length_to,
            probation_length, guideline, points, state, federal, tribal, offenses):
    new_row = {
        'Arrest Date': arrest_date,
        'J/A': ja,
        'Sentence Date': sentence_date,
        'Custody Length Imposed': custody_length_imposed,
        'Custody Length From': custody_length_from,
        'Custody Length To': custody_length_to,
        'Probation Length': probation_length,
        'Guideline': guideline,
        'Points': points,
        'State': state,
        'Federal': federal,
        'Tribal': tribal,
        'Offenses': offenses
    }
    data.append(new_row)
    write_to_csv()


# Function to write data to the CSV file
def write_to_csv():
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"CSV file '{csv_file}' updated successfully.")


# Example usage
add_row('2023-03-01', 'A', '2023-04-01', '36 months', '2023-04-01', '2026-04-01', '24 months', 'Guideline 2', 10, 'NY',
        'No', 'Yes', 'Offense 2')
add_row('2023-05-01', 'H', '2023-06-01', '12 months', '2023-06-01', '2024-06-01', '6 months', 'Guideline 3', 8, 'TX',
        'Yes', 'No', 'Offense 3')
add_row('2023-07-01', 'J', '2023-08-01', '48 months', '2023-08-01', '2027-08-01', '36 months', 'Guideline 4', 15, 'FL',
        'No', 'No', 'Offense 4')

pdf_path = 'USSC_PCR_Sample.pdf'
charges = get_charges_from_sample_pdf(pdf_path)
for i in range(len(charges)):
    print(f"Charge {i + 1}: {charges[i]}")


context = charges[len(charges) - 1]
question = "How old is the defendant?"
# Tokenize the input
inputs = tokenizer(question, context, return_tensors="pt", truncation=True, padding=True)

# Get model output
with torch.no_grad():
    outputs = model(**inputs)

# Extract the answer (start and end token positions)
answer_start = torch.argmax(outputs.start_logits)
answer_end = torch.argmax(outputs.end_logits) + 1
answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))

print(f"""Context: {context}
          Question: {question}
          Answer: {answer}""")


