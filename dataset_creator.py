import random
from utils.llm_qa_util import LLMQAUtil
from utils.psr_extraction_util import get_charges_from_sample_pdf
from utils.psr_csv_util import add_row, ChargeRecord
import re


def multiline_input():
    print("Enter your answer (type 'END' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line == 'END':
            break
        lines.append(line)
    return '\n'.join(lines)


def format_to_json(context, question, answer, answer_start):
    #     formatted_string = f'''
    # {{
    #     "context": "{context}",
    #     "question": "{question}",
    #     "answers": {{
    #       "text": [
    #         "{answer}"
    #       ],
    #       "answer_start": [
    #         {answer_start}
    #       ]
    #     }}
    # }}
    #     '''
    formatted_string = (f'{{"context": "{context.replace('\n', '\\n').replace('"', '\\"')}","question": "{question}",'
                        f'"answers": {{"text": ["{answer.replace('\n', '\\n').replace('"', '\\"')}"],'
                        f'"answer_start": [{answer_start}]}}}}')
    return formatted_string.strip()


def write_string_to_file(string_data, filename='generated_dataset.json'):
    with open(filename, 'w') as file:
        file.write(string_data)


pdf_path = 'USSC_PCR_Sample.pdf'
charges = get_charges_from_sample_pdf(pdf_path)
questions_list = [
    "What age is the person?",
    "How much time in custody?",
    "How much time in probation?",
    "What American State is it?",
    "What offense was committed?"
]

qa_util = LLMQAUtil()
samples = []
for charge in charges:
    context = charge
    random_index = random.randint(0, len(questions_list) - 1)
    random_question = questions_list[random_index]
    print(f"Context:\n{charge}\n\nQuestion:\n{random_question}")
    answer = multiline_input()
    answer_start_index = context.find(answer)
    sample = format_to_json(context, random_question, answer, answer_start_index)
    samples.append(sample)

dataset_string = "["
for i in range(len(samples)):
    dataset_string += samples[i]
    if i != len(samples) - 1:
        dataset_string += ","
dataset_string += "]"

write_string_to_file(dataset_string)
