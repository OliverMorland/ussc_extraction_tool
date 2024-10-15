from utils.llm_qa_util import LLMQAUtil
from utils.psr_extraction_util import get_charges_from_sample_pdf
from utils.psr_csv_util import add_row

# Extract charges from Post Sentencing Report
pdf_path = 'USSC_PCR_Sample.pdf'
charges = get_charges_from_sample_pdf(pdf_path)
# for i in range(len(charges)):
#     print(f"Charge {i + 1}: {charges[i]}")

qa_util = LLMQAUtil()
for charge in charges:
    print("Querying the charge...")
    date = qa_util.query_the_charge("What is the date?", charge)
    age = qa_util.query_the_charge("How old is the person?", charge)
    custody_length = qa_util.query_the_charge("How much time was sentenced in custody?", charge)
    probation_length = qa_util.query_the_charge("How much time was sentenced in probation?", charge)
    offense = qa_util.query_the_charge("What offense is the person charged with?", charge)
    add_row(date, "J/A", "", custody_length, "", "", probation_length,
            "", 0, "", "", "", offense)

# answer = qa_util.query_the_charge("What is the offense of the person?", charges[len(charges) - 1])

# Output Result
# print(f"Context: {charges[len(charges) - 1]}\n\nAnswer: {answer}")
