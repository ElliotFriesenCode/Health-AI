<h1>Condition Predictor / Medicine Recommendation API</h1>

This API allows users to input symptoms and receive recommendations for possible conditions along with Amazon referral links to relevant medicines. The API leverages machine learning to predict conditions based on symptoms and uses web scraping to fetch medicine links from Amazon.

<h3>How to use:</h3>
1. Clone the repository:
2. Install depedendencies
- Flask: Web framework for Python.
 - NLTK: Natural Language Toolkit for text processing.
 - pandas: Data manipulation and analysis library.
 - scikit-learn: Machine learning library.
3. Run train_model.py
4. Run the flask app: python handler.py
5. call the endpoint '/predict'

request body: {  'text': 'youor symptoms' }

response object: {
        "matched_symptoms": symptoms extracted from your description,
        "top_conditions": list of possible predictions,
        "medicines": links to various medicines for your symptoms
}


<h3>How it Works:</h3>

Using NLTK and a fuzzy search, this api extracts symptoms from a patients description. Then it utilizes a random forest classifier to predict conditions and medicines. The dataset used for this project is from a variety of resources such as WebMD and MayoClinic
