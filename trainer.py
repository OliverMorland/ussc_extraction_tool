import json
from datasets import Dataset
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering, Trainer, TrainingArguments


# Load and preprocess the dataset
def load_dataset(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return Dataset.from_list(data)


# Tokenize the inputs for DistilBERT with padding and truncation
def tokenize_function(example):
    return tokenizer(
        example['context'],
        example['question'],
        truncation=True,
        padding='max_length',  # Ensure all sequences have the same length
        max_length=512  # Adjust max length as needed
    )


# Add start and end positions of the answer within the context
def add_token_positions(example):
    start_pos = example['context'].find(example['answer'])
    end_pos = start_pos + len(example['answer'])

    if start_pos == -1:
        # Handle cases where the answer is not found in the context
        start_pos, end_pos = 0, 0

    return {
        'start_positions': start_pos,
        'end_positions': end_pos
    }


# Load the dataset (Replace 'dataset.json' with the actual path to your dataset)
dataset_file = 'expanded_dataset.json'
dataset = load_dataset(dataset_file)

# Initialize the tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-distilled-squad')

# Tokenize the dataset with padding and truncation
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Add token positions (start and end of the answer in the context)
tokenized_dataset = tokenized_dataset.map(add_token_positions)

# Load the pre-trained model for question-answering
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',  # Output directory for saving model checkpoints
    evaluation_strategy="epoch",  # Evaluate at each epoch
    learning_rate=2e-5,  # Learning rate
    per_device_train_batch_size=8,  # Batch size for training
    per_device_eval_batch_size=8,  # Batch size for evaluation
    num_train_epochs=3,  # Number of epochs
    weight_decay=0.01,  # Weight decay
    logging_dir='./logs',  # Directory for logs
    logging_steps=10,  # Log every 10 steps
    save_steps=500,  # Save checkpoint every 500 steps
    save_total_limit=2,  # Only keep the latest 2 checkpoints
)

# Initialize the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,  # In practice, use a separate validation set
    tokenizer=tokenizer
)

# Train the model
trainer.train()

# Save the final model
model.save_pretrained('./psr_trained_model')
tokenizer.save_pretrained('./psr_trained_model')
