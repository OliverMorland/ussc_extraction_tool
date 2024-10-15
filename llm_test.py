from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch

# Load the fine-tuned model
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-distilled-squad')
# model = DistilBertForQuestionAnswering.from_pretrained('./psr_trained_model')
# tokenizer = DistilBertTokenizer.from_pretrained('./psr_trained_model')

# Sample context and query
context = """05/22/1976: 90 days custody
with credit for time served
and the balance of time
suspended and placed on
Community Intervention and
Monitoring Program for 90
days."""
question = "How long is the custody ?"

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
