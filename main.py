from utils.llm_qa_util import LLMQAUtil
from utils.psr_extraction_util import get_charges_from_sample_pdf
from utils.psr_csv_util import add_row, ChargeRecord

# Extract charges from Post Sentencing Report
pdf_path = 'USSC_PCR_Sample.pdf'
charges = get_charges_from_sample_pdf(pdf_path)
# for i in range(len(charges)):
#     print(f"Charge {i + 1}: {charges[i]}")

qa_util = LLMQAUtil()
for charge in charges:
    print("Querying the charge...")
    record = ChargeRecord()
    record.arrest_date = qa_util.query_the_charge("What is the date?", charge)
    record.age = qa_util.query_the_charge("How old is the person?", charge)
    if int(record.age) < 18:
        record.ja = "J"
    else:
        record.ja = "A"
    record.custody_length_imposed = qa_util.query_the_charge("How much time was sentenced in custody?", charge)
    record.probation_length = qa_util.query_the_charge("How much time was sentenced in probation?", charge)
    record.state = qa_util.query_the_charge("What state in the USA is the court location?", charge)
    record.offense = qa_util.query_the_charge("What offense is the person charged with?", charge)
    add_row(record)

# answer = qa_util.query_the_charge("What is the offense of the person?", charges[len(charges) - 1])

# Output Result
# print(f"Context: {charges[len(charges) - 1]}\n\nAnswer: {answer}")
