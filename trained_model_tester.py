from transformers import DistilBertForQuestionAnswering, DistilBertTokenizerFast, DistilBertTokenizer
import torch

# Load the fine-tuned model and tokenizer from the saved directory
model_path = './fine_tuned_distilbert'
# model = DistilBertForQuestionAnswering.from_pretrained(model_path)
# tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-cased-distilled-squad')
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')


# Function to test the model with a new context and question
def answer_question(context, question):
    # Tokenize input
    inputs = tokenizer(question, context, return_tensors='pt', truncation=True, max_length=384)

    # Get model outputs
    with torch.no_grad():  # No need to compute gradients during inference
        outputs = model(**inputs)

    # Extract start and end logits
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits

    # Get the most likely start and end of the answer span
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits)

    # Decode the tokens back to text
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index + 1])
    )

    return answer


test_samples = [
    "09/24/1975\n(Age 15)\nBreaking and Entering (2 counts); Rustle County Juvenile Court, Case No. 2055JD147; Columbus, AL. 11/04/1975: 6 months custody on each count to run consecutively, $50 fine. 03/30/1976: Paroled.",
    "12/20/2016\n(Age 57)\nShoplifting under $100 Brockton District Court; Brockton, MA 01/05/2017: Guilty plea, 1 year unsupervised probation, $35 to victim witness fund.",
    "03/10/2010\n(Age 22)\nAssault with a deadly weapon Franklin County Court; Lexington, KY 05/12/2010: Guilty, 2 years probation $100 fine."
]

# Test the model with a new context and question
context = ("09/24/1975\n(Age 15)\nBreaking and Entering (2 counts); Rustle County Juvenile Court, Case No. 2055JD147; "
           "Columbus, AL. 11/04/1975: 6 months custody on each count to run consecutively, $50 fine. 03/30/1976: "
           "Paroled.")
question = "What state is it in?"

# Get the answer from the model
# answer = answer_question(context, question)

for sample in test_samples:
    answer = answer_question(sample, question)
    print(f"Context: {sample}")
    print(f"Question: {question}")
    print(f"Answer: {answer}")

# Print the answer
# print(f"Question: {question}")
# print(f"Answer: {answer}")
