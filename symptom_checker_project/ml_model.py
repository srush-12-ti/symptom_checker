import json
import joblib
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Step 1: Load training data
with open("feedback_data.json") as f:
    data = json.load(f)

# Step 2: Filter only 'yes' feedback
filtered = [d for d in data if d["user_feedback"] == "yes"]

# Step 3: Separate symptoms and labels
X = [d["symptoms"] for d in filtered]
y = [d["predicted_disease"] for d in filtered]

# Step 4: Define all possible symptoms
all_symptoms = [
    "fever", "headache", "body pain", "cough", "sore throat", "fatigue",
    "sneezing", "runny nose", "chills", "nausea", "vomiting", "sweating",
    "dry cough", "loss of taste", "loss of smell", "breathing difficulty",
    "mild cough"
]

# Step 5: Encode symptoms using MultiLabelBinarizer
mlb = MultiLabelBinarizer()
mlb.fit([all_symptoms])
X_encoded = mlb.transform(X)

# Step 6: Split the data
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
print("Train labels:", set(y_train))
print("Test labels:", set(y_test))

# Step 7: Train the model
model = MultinomialNB()
model.fit(X_train, y_train)

# Step 8: Evaluate
y_pred = model.predict(X_test)
print("Model accuracy:", accuracy_score(y_test, y_pred))

# Step 9: Save the model and encoder
joblib.dump(model, "model.pkl")
joblib.dump(mlb, "mlb.pkl")
