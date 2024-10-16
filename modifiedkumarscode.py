import fitz  # PyMuPDF
import pandas as pd
import re


# Function to convert text-based duration to months
def convert_to_months(text):
    match = re.search(r'(\d+)\s*(year|month)', text, re.IGNORECASE)
    if match:
        value = int(match.group(1))
        unit = match.group(2).lower()
        if 'year' in unit:
            return value * 12
        return value
    return 0


def split_match(match):
    merged_match = " ".join(match)
    return split_match


# Read the PDF file
# pdf_path = 'pdfs/SampleCriminalHistory.pdf'
pdf_path = 'SampleCriminalHistory.pdf'
document = fitz.open(pdf_path)

# Extract text from each page
text = ""
for page_num in range(len(document)):
    page = document.load_page(page_num)
    text += page.get_text()

# Ensure the section headers exist
if "Juvenile Adjudication(s)" in text and "Adult Criminal Conviction(s)" in text:
    print("Both sections found in the text.")
else:
    print("Sections not found. Check the text extraction.")

# Manually find the sections based on headers
juvenile_start = text.find("Juvenile Adjudication(s)")
adult_start = text.find("Adult Criminal Conviction(s)")
juvenile_end = adult_start if adult_start != -1 else len(text)
adult_end = text.find("Other Criminal Conduct") if "Other Criminal Conduct" in text else len(text)

# Extract sections based on identified indices
juvenile_section = text[juvenile_start:juvenile_end].strip()
adult_section = text[adult_start:adult_end].strip()

print("Adult Section:\n", adult_section)  # Print extracted adult section

# Define regex patterns to extract individual records
juvenile_pattern = re.compile(
    r'\d+\.\s+\d{2}/\d{2}/\d{4}.*?(?=\d+\.\s+\d{2}/\d{2}/\d{4}|Juvenile Adjudication|Adult Criminal Conviction|\n\n|$)',
    re.S)
# adult_pattern = re.compile(r'(\d+\.\s+\d{2}/\d{2}/\d{4}.*?)(?=\d+\.\s+\d{2}/\d{2}/\d{4}|Other Criminal Conduct|\n\n|$)', re.S)
#modified adult regex
adult_pattern = re.compile(
    r'(\d+\.\s+\d{2}/\d{2}/\d{4}.*?)(?=\n\d+\.\s+\d{2}/\d{2}/\d{4}|\nOther Criminal Conduct|\n\n|$)', re.S)

print("ADULT_SECTION", adult_section)
juvenile_matches = juvenile_pattern.findall(juvenile_section)
adult_matches = adult_pattern.findall(adult_section)

print(f"Juvenile Matches: {len(juvenile_matches)} records")
print(f"Adult Matches len: {len(adult_matches)} records")
print("Adult Matches:", adult_matches)  # Print the matches for debugging


def extract_data(matches, juvenile=True):
    data = []
    for match in matches:
        print("Processing match:", match)  # Debug log
        lines = match.strip().split("\n")
        joined_match = " ".join(lines)
        print("joined_match", joined_match)

        # Extract arrest date (first date)
        arrest_date_match = re.search(r'\d{2}/\d{2}/\d{4}', match)
        arrest_date = arrest_date_match.group() if arrest_date_match else "."
        print("Arrest Date:", arrest_date)  # Debug log

        # Extract offense (from the second line if available)
        offense = lines[1].strip() if len(lines) > 1 else "."
        print("Offense:", offense)  # Debug log

        # Determine Juvenile or Adult
        ja_type = "J" if juvenile else "A"

        # Extract age
        age_match = re.search(r'\(Age\s*(\d+)\s*\)', match)
        age = age_match.group(1) if age_match else "."
        print("Age:", age)  # Debug log

        # Extract initial sentence date from the middle column
        sentence_date = "."
        for line in lines[2:]:
            sentence_date_match = re.search(r'\d{2}/\d{2}/\d{4}', line)
            if sentence_date_match and sentence_date == ".":
                sentence_date = sentence_date_match.group()
            elif sentence_date != ".":
                break

        # Extract custody length imposed
        custody_length_imposed = "."
        for line in lines:
            if "custody" in line.lower():
                custody_length_imposed = convert_to_months(line)
                break

        # Extract probation length
        probation_length = 0
        for line in lines:
            if "probation" in line.lower():
                probation_length = convert_to_months(line)
                break

        # # Old Extract guideline
        # guideline = "."
        # guideline_matches = re.findall(r'4[A-Z]\d+\.\d+\([a-z]\)', ' '.join(lines))
        # if not guideline_matches:
        #     guideline_matches = re.findall(r'4[A-Z]\d+\.\d+', ' '.join(lines))
        # if guideline_matches:
        #     guideline = ', '.join(set(guideline_matches))  # Ensure unique guidelines

        #New Extrac guideline
        guideline = "."
        guideline_matches = re.findall(r'\d[A-Z]\d\.\d\([a-z]\)\(\d\) | \d[A-Z]\d\.\d\([a-z]\)\s+', joined_match)
        if not guideline_matches:
            guideline_matches = re.findall(r'4[A-Z]\d+\.\d+', ' '.join(lines))
        if guideline_matches:
            guideline = ', '.join(set(guideline_matches))  # Ensure unique guidelines

        # extract points
        points_match = re.search(r'\d[a-zA-Z]\d\.\d\([a-zA-Z]\)\(\d\)\s+(\d+)|\d[a-zA-Z]\d\.\d\([a-zA-Z]\)\s+(\d+)',
                                 joined_match)
        points = points_match.group(1) if points_match and points_match.group(1) else (
            points_match.group(2) if points_match and points_match.group(2) else "0")

        # Extract state
        state = "."
        for line in lines:
            state_match = re.search(r'\b[A-Z]{2}\b', line)
            if state_match:
                state = state_match.group()
                break

        data.append(
            [arrest_date, ja_type, age, sentence_date, custody_length_imposed, ".", ".", probation_length, guideline,
             points, state, ".", ".", "."])
        print(f"Extracted data: {data[-1]}")  # Logging for debugging
    return data


# Process juvenile and adult events
juvenile_data = extract_data(juvenile_matches, juvenile=True)  # Extract all juvenile matches
adult_data = extract_data(adult_matches, juvenile=False)  # Extract all adult matches

# Create DataFrames
columns = ["Arrest Date", "J/A", "Age", "Sentence Date", "Custody Length Imposed", "Custody Length From",
           "Custody Length To", "Probation Length", "Guideline", "Points", "State", "Federal", "Tribal Court",
           "Offenses"]

juvenile_df = pd.DataFrame(juvenile_data, columns=columns)
adult_df = pd.DataFrame(adult_data, columns=columns)

# Display DataFrames
print("Juvenile Events")
print(juvenile_df)
print("\nAdult Events")
print(adult_df)

total_df = pd.concat([juvenile_df, adult_df], axis=0)
total_df.to_csv("Results.csv", index=False)
