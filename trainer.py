from transformers import DistilBertForQuestionAnswering, DistilBertTokenizerFast, Trainer, TrainingArguments
from datasets import load_dataset

# Load the pre-trained model and tokenizer
model_to_train = './custody_trained_distilbert'
model = DistilBertForQuestionAnswering.from_pretrained(model_to_train)
tokenizer = DistilBertTokenizerFast.from_pretrained(model_to_train)

# Load your custom dataset
dataset = load_dataset('json', data_files={'train': 'dataset_500.json'})


# Tokenize the inputs
def preprocess_function(examples):
    # Tokenize the inputs
    questions = [q.strip() for q in examples['question']]
    inputs = tokenizer(
        questions,
        examples['context'],
        max_length=384,
        truncation="only_second",
        return_offsets_mapping=True,
        padding="max_length",
    )

    # Extracting the correct answer positions
    start_positions = []
    end_positions = []

    for i, offset in enumerate(inputs['offset_mapping']):
        # Access the answers correctly from the list
        start_char = examples['answers'][i]['answer_start'][0]  # First answer start position
        end_char = start_char + len(examples['answers'][i]['text'][0])  # End position based on answer text length
        sequence_ids = inputs.sequence_ids(i)

        token_start = None
        token_end = None

        # Iterate through sequence_ids and offsets to find token positions
        for idx, (seq_id, offset_pair) in enumerate(zip(sequence_ids, offset)):
            if seq_id == 1 and offset_pair[0] <= start_char and offset_pair[1] > start_char:
                token_start = idx
            if seq_id == 1 and offset_pair[0] < end_char and offset_pair[1] >= end_char:
                token_end = idx

        # Handle cases where token_start or token_end is None
        if token_start is None:
            token_start = 0  # You can choose a default like 0
        if token_end is None:
            token_end = 0  # You can choose a default like 0

        start_positions.append(token_start)
        end_positions.append(token_end)

    inputs['start_positions'] = start_positions
    inputs['end_positions'] = end_positions
    return inputs


# Apply preprocessing to your dataset
tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=['context', 'question', 'answers'])

# Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="no",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Set up the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train']
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model_path = './custody_and_state_trained_distilbert'
trainer.save_model(model_path)
tokenizer.save_pretrained(model_path)
