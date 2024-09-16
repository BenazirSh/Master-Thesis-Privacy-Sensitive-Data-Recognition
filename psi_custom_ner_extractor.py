import os
import re
import json
import random
from transformers import pipeline

# Regular expressions for identifying PSIs (first name, last name, date of birth, gender, etc.)
regex_patterns = {
    "First Name": r"\b(?!(Mr|Ms|Mrs|Dr|Mx)\b)([A-Z][a-z]+)\b",
    "Last Name": r"\b(?!Ms|Mr|Mrs|Dr|Mx)\b([A-Z][a-z]+)\b",
    "Date of Birth": r"\b(?:\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}|\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2})\b",
    "Gender": r"\b(Male|Female|Other)\b",
    "Age": r"\b\d{2}\syears old\b",
    "Nationality": r"\b(?:Nationality|Citizenship)?\s?:?\s?(American|British|Canadian|French|German|Italian"
                   r"|Mexican|Indian|Chinese|Japanese|Australian|Spanish"
                   r"|Brazilian|Russian|South African|Nigerian|Egyptian"
                   r"|Dutch|Greek|Swedish|Norwegian|Finnish|Polish|Korean"
                   r"|Vietnamese|Thai|Indonesian|Filipino|Argentinian"
                   r"|Turkish|Portuguese|Colombian|Chilean|Peruvian"
                   r"|Saudi Arabian|Iranian|Iraqi|Pakistani|Afghan|Bangladeshi|Malaysian|Somali|Kenyan)\b",
    "Marital Status": r"\b(Single|Married|Divorced|Widowed)\b"
}

# Define a simple NER model using Hugging Face's pipeline for organization, education, and work experience extraction
ner_model = pipeline("ner", model="bert-ner-fine-tuned-with-educational-institutions", aggregation_strategy="simple")


def generate_random_name():
    first_name = ''.join(
        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + random.choice('aeiou') + random.choice('bcdfghjklmnpqrstvwxyz')
        for _ in range(1))
    last_name = ''.join(
        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + random.choice('aeiou') + random.choice('bcdfghjklmnpqrstvwxyz')
        for _ in range(2))
    return f"{first_name} {last_name}"


def generate_random_location():
    city_prefixes = ['New', 'Old', 'North', 'South', 'Port', 'Lake', 'Fort']
    city_suffixes = ['ton', 'ville', 'land', 'city', 'borough', 'haven']
    countries = ['USA', 'Canada', 'Germany', 'France', 'Italy', 'Spain', 'Australia', 'Japan', 'Sudan',
                 'Chad', 'Morocco', 'Latvia', 'Romania', 'Turkey', 'Uzbekistan', 'Azerbaijan']

    city = random.choice(city_prefixes) + random.choice(city_suffixes)
    country = random.choice(countries)
    return f"{city}, {country}"


def combine_city_country(locations):
    combined_locations = []
    i = 0
    while i < len(locations):
        if i < len(locations) - 1:
            combined_locations.append(f"{locations[i]}, {locations[i + 1]}")
            i += 2
        else:
            combined_locations.append(locations[i])
            i += 1
    return combined_locations


def anonymize_psi(psi_dict):
    anonymized_psi = {}
    for key, value in psi_dict.items():
        if isinstance(value, list):
            if key == "Location":
                combined_locations = combine_city_country(value)
                anonymized_psi[key] = [generate_random_location() for _ in combined_locations]
            elif key == "Person":
                anonymized_psi[key] = [generate_random_name() for _ in value]
            else:
                anonymized_psi[key] = ["*" * len(word) for word in value]
        else:
            anonymized_psi[key] = "*" * len(value)
    return anonymized_psi


# Function to extract PSIs using regular expressions
def extract_psi_with_regex(text, patterns):
    extracted_psi = {}
    first_name_match = re.search(patterns['First Name'], text)
    if first_name_match:
        extracted_psi['First Name'] = first_name_match.group(0)
        text = text.replace(first_name_match.group(0), '', 1)

    last_name_match = re.search(patterns['Last Name'], text)
    if last_name_match:
        extracted_psi['Last Name'] = last_name_match.group(0)

    for psi_name, pattern in patterns.items():
        if psi_name not in ['First Name', 'Last Name']:
            match = re.search(pattern, text)
            if match:
                extracted_psi[psi_name] = match.group(0)

    return extracted_psi


# Function to extract entities using BERT NER
def extract_psi_with_bert(text):
    ner_results = ner_model(text)
    extracted_psi = {"Organization": [], "Education": [], "Location": [], "Person": []}
    for entity in ner_results:
        if entity["entity_group"] == "ORG":
            extracted_psi["Organization"].append(entity["word"])
        elif entity["entity_group"] == "PER":
            extracted_psi["Person"].append(entity["word"])
        elif entity["entity_group"] == "LOC":
            extracted_psi["Location"].append(entity["word"])
        elif entity["entity_group"] == "EDU":
            extracted_psi["Education"].append(entity["word"])
    return extracted_psi


# Main function to process a CV and extract PSIs from all sections
def process_cv(cv_data):
    psi_results = {}
    cv_text = ""

    for section in cv_data.values():
        if isinstance(section, list):  # For sections that are lists of text
            for entry in section:
                if 'text' in entry:
                    cv_text += entry['text'] + " "
        elif isinstance(section, dict):  # For sections that may be dictionaries
            if 'text' in section:
                cv_text += section['text'] + " "

    psi_results.update(extract_psi_with_regex(cv_text, regex_patterns))
    psi_results.update(extract_psi_with_bert(cv_text))

    return psi_results


# Function to load and process CVs from the resources directory
def load_and_process_cvs():
    resource_dir = os.path.join(os.path.dirname(__file__), 'resources', 'CVs')
    for cv_file in os.listdir(resource_dir):
        cv_path = os.path.join(resource_dir, cv_file)
        with open(cv_path, 'r') as file:
            cv_data = json.load(file)
            cv_content = list(cv_data.values())[0]

            psi = process_cv(cv_content)
            print(f"PSI for {cv_file}: {psi}")

            anonymized_psi = anonymize_psi(psi)
            print(f"Anonymized PSI for {cv_file}: {anonymized_psi}\n")


# Run the processing function
if __name__ == "__main__":
    load_and_process_cvs()
