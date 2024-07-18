from predit_symptoms import match_symptoms
from predict_conditions import get_links_by_symptom, predict_top_conditions
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import spacy

nlp = spacy.load('en_core_web_md')

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_sentence = data['text']
   
    matched_symptoms = match_symptoms(input_sentence) 
# get symptoms
    if matched_symptoms:
        input_doc = nlp(input_sentence)
        symptom_similarities = []
        for symptom in matched_symptoms:
           symptom_doc = nlp(symptom)
           similarity = input_doc.similarity(symptom_doc)
           symptom_similarities.append((symptom, similarity))
           print(symptom_similarities)
           print(f"Matched Symptoms: {matched_symptoms}")
        else:
             print("No matching symptom found.")


# get conditions

    top_conditions = predict_top_conditions(matched_symptoms)
    print(f"Top 3 Predicted Conditions: {top_conditions}")

# get medicines

    for symptom in matched_symptoms:
      links = get_links_by_symptom(symptom)
      if links:
        print(f"Links for {symptom}: {links}")
      else:
         print(f"No links found for symptom: {symptom}")
        
    response_data = {
        "matched_symptoms": symptom_similarities,
        "top_conditions": top_conditions,
        "medicines": links
    }
    print(response_data)
    json_response = json.dumps(response_data)
    return json_response
    

if __name__ == '__main__':
    app.run(debug=True)