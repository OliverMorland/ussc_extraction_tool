from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch


class LLMQAUtil:
    def __init__(self):
        self.model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-distilled-squad')

    def query_the_charge(self, question, context):
        # Tokenize the input
        inputs = self.tokenizer(question, context, return_tensors="pt", truncation=True, padding=True)

        # Get model output
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Extract the answer (start and end token positions)
        answer_start = torch.argmax(outputs.start_logits)
        answer_end = torch.argmax(outputs.end_logits) + 1
        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))
        return answer
