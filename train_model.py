import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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

# Convert symptoms to a list of lists
symptoms_list = symptoms.values.tolist()

# Use MultiLabelBinarizer to perform one-hot encoding
mlb = MultiLabelBinarizer()
symptoms_encoded = mlb.fit_transform(symptoms_list)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test, rarity_train, rarity_test = train_test_split(symptoms_encoded, conditions, rarity, test_size=0.2, random_state=42)

# Train a Random Forest Classifier and save the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model to a file
joblib.dump(model, 'random_forest_model.joblib')
# Save the MultiLabelBinarizer
joblib.dump(mlb, 'mlb_encoder.joblib')


# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
