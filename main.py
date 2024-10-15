from utils.llm_qa_util import LLMQAUtil
from utils.psr_extraction_util import get_charges_from_sample_pdf

# Extract charges from Post Sentencing Report
pdf_path = 'USSC_PCR_Sample.pdf'
charges = get_charges_from_sample_pdf(pdf_path)
# for i in range(len(charges)):
#     print(f"Charge {i + 1}: {charges[i]}")

qa_util = LLMQAUtil()
answer = qa_util.query_the_charge("What is the offense of the person?", charges[len(charges) - 1])

# Output Result
print(f"Context: {charges[len(charges) - 1]}\n\nAnswer: {answer}")
