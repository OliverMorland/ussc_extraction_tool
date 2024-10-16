import torch
from transformers import DistilBertTokenizerFast, DistilBertForQuestionAnswering

# Load the fine-tuned model and tokenizer
model_path = "./date_trained_distilbert"  # Update this path if different
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForQuestionAnswering.from_pretrained(model_path)


def get_state_from_address(context, question="In what state is the court?"):
    # Tokenize input context and question
    inputs = tokenizer(question, context, return_tensors="pt")

    # Get model outputs
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the most likely start and end positions of the answer
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1

    # Convert tokens to string
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
    )
    return answer


# Test the model on sample contexts
test_samples = [
    "09/24/1975\n(Age 15)\nBreaking and Entering (2 counts); Rustle County Juvenile Court, Case No. 2055JD147; Columbus, AL. 11/04/1975: 6 months custody on each count to run consecutively, $50 fine. 03/30/1976: Paroled.",
    "12/20/2016\n(Age 57)\nShoplifting under $100 Brockton District Court; Brockton, MA 01/05/2017: Guilty plea, 1 year unsupervised probation, $35 to victim witness fund.",
    "03/10/2010\n(Age 22)\nAssault with a deadly weapon Franklin County Court; Lexington, KY 05/12/2010: Guilty, 2 years probation $100 fine."
]

# Print results for each test sample
for context in test_samples:
    state = get_state_from_address(context)
    print(f"Context: {context}\nExtracted State: {state}\n")
