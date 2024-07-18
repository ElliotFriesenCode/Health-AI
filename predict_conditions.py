import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import json
import joblib

# Load the data
data = pd.read_csv('symptoms_and_conditions.csv')
data = data.astype(str)
# Drop unnecessary columns, but keep the 'Rarity' column
data = data.drop(columns=['Gender', 'Typical Minimum Age', 'Typical Maximum Age'])

# Extract symptoms, condition, and rarity
symptoms = data.drop(columns=['Condition', 'Rarity'])
conditions = data['Condition']
rarity = data['Rarity']


# Load the trained model and MultiLabelBinarizer from the file
model = joblib.load('./in_use/random_forest_model.joblib')
mlb = joblib.load('./in_use/mlb_encoder.joblib')

# Define rarity weights
rarity_weights = {
    'Common': 1.0,
    'Uncommon': 0.75,
    'Rare': 0.5,
    'Very rare': 0.25
}

# Function to predict condition based on new symptoms and return the top 3 predictions
def predict_top_conditions(new_symptoms, top_n=10):
    # Encode the new symptoms
    new_symptoms_encoded = mlb.transform([new_symptoms])
    # Predict the probabilities for each condition
    probabilities = model.predict_proba(new_symptoms_encoded)[0]
    
    # Get the rarity for each condition
    condition_rarity = dict(zip(conditions, rarity))
    
    # Adjust probabilities based on rarity weights
    adjusted_probabilities = []
    for condition, prob in zip(model.classes_, probabilities):
        weight = rarity_weights.get(condition_rarity[condition], 1.0)
        adjusted_probabilities.append(prob * weight)
    
    # Get the indices of the top N conditions
    top_indices = sorted(range(len(adjusted_probabilities)), key=lambda i: adjusted_probabilities[i], reverse=True)[:top_n]
    
    # Get the top N conditions
    top_conditions = [(model.classes_[i], adjusted_probabilities[i]) for i in top_indices]
    return top_conditions

with open('symptoms_with_links.json', 'r') as file:
    datajson = json.load(file)

def get_links_by_symptom(symptom_name):
    for item in datajson:
        if item["symptom"] == symptom_name:
            return item["links"]
    return None

