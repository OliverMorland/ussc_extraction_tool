import csv

data = []

# Define the CSV file name
csv_file = 'output.csv'

# Define the column names
columns = [
    'Arrest Date', 'J/A', 'Age', 'Sentence Date', 'Custody Length Imposed', 'Custody Length From',
    'Custody Length To', 'Probation Length', 'Guideline', 'Points', 'State', 'Federal',
    'Tribal', 'Offenses'
]


class ChargeRecord:
    arrest_date = ""
    ja = ""
    age = ""
    sentence_date = ""
    custody_length_imposed = ""
    custody_length_from = ""
    custody_length_to = ""
    probation_length = ""
    guideline = ""
    points = ""
    state = ""
    federal = ""
    tribal = ""
    offense = ""


# Function to add a row to the data
def add_row(record: ChargeRecord):
    new_row = {
        'Arrest Date': record.arrest_date,
        'J/A': record.ja,
        'Age': record.age,
        'Sentence Date': record.sentence_date,
        'Custody Length Imposed': record.custody_length_imposed,
        'Custody Length From': record.custody_length_from,
        'Custody Length To': record.custody_length_to,
        'Probation Length': record.probation_length,
        'Guideline': record.guideline,
        'Points': record.points,
        'State': record.state,
        'Federal': record.federal,
        'Tribal': record.tribal,
        'Offenses': record.offense
    }
    data.append(new_row)
    write_to_csv()


# Function to write data to the CSV file
def write_to_csv():
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"CSV file '{csv_file}' updated successfully.")

# add_row('2023-03-01', 'A', '2023-04-01', '36 months', '2023-04-01', '2026-04-01', '24 months', 'Guideline 2', 10, 'NY',
#         'No', 'Yes', 'Offense 2')
# add_row('2023-05-01', 'H', '2023-06-01', '12 months', '2023-06-01', '2024-06-01', '6 months', 'Guideline 3', 8, 'TX',
#         'Yes', 'No', 'Offense 3')
# add_row('2023-07-01', 'J', '2023-08-01', '48 months', '2023-08-01', '2027-08-01', '36 months', 'Guideline 4', 15, 'FL',
#         'No', 'No', 'Offense 4')
