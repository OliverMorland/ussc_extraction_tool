import json
import random


# Function to convert years and months into a text string
def convert_to_sentence(years=None, months=None):
    if years and months:
        return f"{years} years and {months} months"
    elif years:
        return f"{years} years"
    elif months:
        return f"{months} months"
    else:
        return None


# Function to generate the answer in months based on the given years and months
def generate_answer(years=None, months=None):
    total_months = 0
    if years:
        total_months += years * 12
    if months:
        total_months += months
    return f"{total_months} months"


# Function to generate a random sentencing entry
def generate_entry():
    years = random.choice([None, random.randint(1, 15)])  # Randomly choose between 1 and 15 years or None
    months = random.choice([None, random.randint(1, 11)]) if years else random.randint(1, 11)  # Add months if no years

    sentence = convert_to_sentence(years, months)
    answer = generate_answer(years, months)

    context_templates = [
        f"11/04/1975: {sentence} custody on each count o run consecutively, $50 fine.",
        f"""05/22/1976: {sentence} custody with credit for time served and the balance of time suspended and placed 
        on Community Intervention and Monitoring Program for 90 days.""",
        f"""10/23/1980: Guilty plea, {sentence} Imprisonment""",
        f"""09/17/2015: Supervised release revoked. {sentence} custody, credit for time served, no TSR to follow""",
        f"A {sentence} custody was given for the charges.",
        f"The judge handed down a sentence of {sentence} jail time",
        f"For the crime, the court sentenced the individual to {sentence} in jail.",
    ]

    context = random.choice(context_templates)
    entry = {
        "context": context,
        "question": "How long was the sentence?",
        "answer": answer
    }
    return entry


# Generate 400 dataset entries
def generate_dataset(num_entries=1000):
    dataset = []
    for _ in range(num_entries):
        dataset.append(generate_entry())
    return dataset


# Save the dataset to a JSON file
dataset = generate_dataset()

# Save dataset to a file named 'expanded_dataset.json'
with open('expanded_dataset.json', 'w') as f:
    json.dump(dataset, f, indent=4)

print(f"Dataset created and saved to 'expanded_dataset.json'.")
