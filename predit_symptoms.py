import json
from fuzzywuzzy import fuzz

# Load symptoms from JSON file
with open('symptoms_with_synonyms.json', 'r') as file:
    symptoms = json.load(file)

# Function to match input sentence with keywords or their synonyms
def match_symptoms(sentence):
    matched_symptoms = []
    for item in symptoms:
        keywords = [item["keyword"]] + [synonym for synonym in item.get("keyword_synonyms", []) if len(synonym) > 3]
        for keyword in keywords:
            if fuzz.partial_ratio(sentence.lower(), keyword.lower()) > 90:  # Adjust the threshold as needed
                print(f"Symptom: {item['symptom']} matches with keyword: {keyword}")
                matched_symptoms.append(item['symptom'])
                break  # Move to the next symptom after finding a match
    return matched_symptoms
