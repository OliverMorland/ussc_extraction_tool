from transformers import DistilBertForQuestionAnswering, DistilBertTokenizerFast, DistilBertTokenizer
import torch

# Load the fine-tuned model and tokenizer from the saved directory
model_path = './state_trained_distilbert'
model = DistilBertForQuestionAnswering.from_pretrained(model_path)
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)


# model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-cased-distilled-squad')
# tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')


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


def get_answers_for_question(question, samples):
    for sample in samples:
        answer = answer_question(sample, question)
        print(f"Context: {sample}")
        print(f"Question: {question}")
        print(f"Answer: {answer}")


test_samples = [
    """06/01/1980
(Age 21)
Larceny of Property
$250 or Less
Brockton
Municipal Court;
Brockton, MA
10/23/1980:
Guilty plea, 2-5 yrs.
Imprisonment
06/10/1981:
Paroled
12/24/1981: Parole
Revoked, 6 months’
imprisonment, released at
expiration
4A1.2(e)(3) 0""",
    """12/20/2016
(Age 57)
Shoplifting under
$100 Brockton
District Court;
Brockton, MA
01/05/2017: Guilty plea, 1
year unsupervised probation,
$35 to victim witness fund
4A1.1(c) 1""",
    """02/16/2014
(Age 55)
Uttering a
Counterfeit
Instrument and
Attempt to Utter a
Counterfeit
Instrument.
US District Court,
District of
Massachusetts;
Cincinatti, OH
06/23/2014:
Guilty plea, time served, 3
years supervised release,
$251 restitution, $100
Special Assessment
09/17/2015: Supervised
release revoked. 3 months’
custody, credit for time
served, no TSR to follow
4A1.1(b)"""
]

# Test the model with a new context and question
custody_question = "How much time in custody was sentenced?"
state_question = "What American State is it?"
probation_question = "How much time in probation was sentenced?"

# Get the answer from the model
# answer = answer_question(context, question)


get_answers_for_question(state_question, test_samples)

# Print the answer
# print(f"Question: {question}")
# print(f"Answer: {answer}")
