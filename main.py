from utils.llm_qa_util import LLMQAUtil
from utils.psr_extraction_util import get_charges_from_sample_pdf
from utils.psr_csv_util import add_row, ChargeRecord
import re


def extract_age(age_string):
    match = re.search(r'\bAge (\d+)\b', age_string)
    if match:
        return int(match.group(1))
    else:
        raise ValueError("No age found in the string")


def find_first_date(text):
    # Regular expression pattern to match dates in the format 'MM/DD/YYYY'
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'

    # Search for the first occurrence of the date pattern
    match = re.search(date_pattern, text)

    if match:
        return match.group(0)
    else:
        return None


def find_guidelines(text):
    # Regular expression pattern to match (number letter number).digit(s)(letter)(optional digit(s))
    pattern = r'4A1\.\d{1}\(.\)(?:\(\d+\))?'

    # Find all matches in the text
    matches = re.findall(pattern, text)

    return matches


# Extract charges from Post Sentencing Report
pdf_path = 'USSC_PCR_Sample.pdf'
charges = get_charges_from_sample_pdf(pdf_path)
# for i in range(len(charges)):
#     print(f"Charge {i + 1}: {charges[i]}")

qa_util = LLMQAUtil()


for charge in charges:
    print("Querying the charge...")
    record = ChargeRecord()

    # Age
    age_string = qa_util.query_the_charge("How old is the person?", charge)
    age_number = extract_age(age_string)
    record.age = str(age_number)

    # Arrest date
    # record.arrest_date = qa_util.query_the_charge("What is the date?", charge)
    record.arrest_date = find_first_date(charge)

    # J or A
    if int(age_number) < 18:
        record.ja = "J"
    else:
        record.ja = "A"

    # Custody length
    record.custody_length_imposed = qa_util.query_the_charge("How much time was sentenced in custody?", charge)

    # Probation length
    record.probation_length = qa_util.query_the_charge("How much time was sentenced in probation?", charge)

    # State of trial
    record.state = qa_util.query_the_charge("What American State is it?", charge)

    # Guideline
    record.guideline = str(find_guidelines(charge))

    # Offense description
    record.offense = qa_util.query_the_charge("What offense is the person charged with?", charge)

    # Add row
    add_row(record)

# answer = qa_util.query_the_charge("What is the offense of the person?", charges[len(charges) - 1])

# Output Result
# print(f"Context: {charges[len(charges) - 1]}\n\nAnswer: {answer}")
