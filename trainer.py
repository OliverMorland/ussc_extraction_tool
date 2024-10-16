import torch
from datasets import load_dataset
from transformers import DistilBertTokenizerFast, DistilBertForQuestionAnswering, Trainer, TrainingArguments

# Load the dataset
dataset_path = 'dataset_50.json'  # Path to the dataset
data = load_dataset('json', data_files=dataset_path)

# Load pre-trained tokenizer and model
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased')


# Preprocess the data
def preprocess_function(examples):
    # Tokenize the inputs (question + context)
    inputs = tokenizer(
        examples['question'],
        examples['context'],
        truncation=True,  # Ensure truncation
        padding="max_length",  # Ensure padding to max_length
        max_length=512,  # Set a maximum length for padding/truncation
    )

    # Extract the start and end positions from each answer in the batch
    start_positions = []
    end_positions = []

    for i in range(len(examples['answers'])):
        start = examples['answers'][i]['answer_start']  # Get the start position (already flat)
        end = start + len(examples['answers'][i]['text']) - 1  # Calculate the end position
        start_positions.append(start)
        end_positions.append(end)

    # Add start and end positions to the inputs
    inputs['start_positions'] = start_positions
    inputs['end_positions'] = end_positions

    return inputs


# Apply the preprocessing function to the dataset
tokenized_data = data.map(preprocess_function, batched=True)

# Split the data into train and eval sets
train_test_split = tokenized_data['train'].train_test_split(test_size=0.2)
train_dataset = train_test_split['train']
eval_dataset = train_test_split['test']

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",  # Evaluate at the end of each epoch
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    save_steps=1000,
    save_total_limit=2,
    remove_unused_columns=False,  # Prevent automatic column removal
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
)

# Train the model
trainer.train()

# Evaluate the model
trainer.evaluate()

# Save the trained model
model.save_pretrained('./fine_tuned_distilbert_state_identifier')
tokenizer.save_pretrained('./fine_tuned_distilbert_state_identifier')

print("Training and evaluation complete. Model saved!")
