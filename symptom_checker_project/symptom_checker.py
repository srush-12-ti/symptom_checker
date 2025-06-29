import json
import os
import joblib
from sklearn.preprocessing import MultiLabelBinarizer

# Load model and encoder if they exist
try:
    model = joblib.load("model.pkl")
    encoder = joblib.load("mlb.pkl")
    ml_ready = True
except:
    model = None
    encoder = None
    ml_ready = False

# Rule-based knowledge
disease_rules = {
    "Flu": ["fever", "headache", "body pain", "cough"],
    "Common Cold": ["sneezing", "runny nose", "sore throat"],
    "Malaria": ["fever", "chills", "sweating", "nausea"],
    "COVID-19": ["fever", "dry cough", "loss of taste", "fatigue"]
}

FEEDBACK_FILE = "feedback_data.json"

def ask_symptoms():
    symptoms = []
    print("\nPlease answer YES or NO to the following symptoms:")
    all_symptoms = sorted({s for lst in disease_rules.values() for s in lst})
    for symptom in all_symptoms:
        ans = input(f"Do you have {symptom}? ").strip().lower()
        if ans == "yes":
            symptoms.append(symptom)
    return symptoms

def diagnose(symptoms):
    matched = {}
    for disease, rule_symptoms in disease_rules.items():
        common = set(symptoms) & set(rule_symptoms)
        matched[disease] = len(common) / len(rule_symptoms)
    return sorted(matched.items(), key=lambda x: x[1], reverse=True)

def display_results(diagnosis):
    print("\nPossible diagnoses:")
    for disease, score in diagnosis:
        if score > 0:
            print(f"- {disease}: {score * 100:.1f}% match")

def get_user_feedback(symptoms, top_disease):
    feedback = input(f"Is the prediction '{top_disease}' correct? (yes/no): ").strip().lower()
    if feedback == "yes":
        update_knowledge_base(symptoms, top_disease)
    store_feedback(symptoms, top_disease, feedback)

def update_knowledge_base(symptoms, disease):
    for symptom in symptoms:
        if symptom not in disease_rules[disease]:
            disease_rules[disease].append(symptom)

def store_feedback(symptoms, disease, feedback):
    entry = {
        "symptoms": symptoms,
        "predicted_disease": disease,
        "user_feedback": feedback
    }
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w") as f:
            json.dump([entry], f, indent=2)
    else:
        with open(FEEDBACK_FILE, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

def predict_with_ml(symptoms):
    if not ml_ready:
        print("ML model not ready or not trained.")
        return None

    input_vector = encoder.transform([symptoms])
    prediction = model.predict(input_vector)
    return prediction[0]

def main():
    print(" Welcome to the Self-Learning Symptom Checker!")
    symptoms = ask_symptoms()

    if ml_ready:
        prediction = predict_with_ml(symptoms)
        print(f"\n ML Prediction: {prediction}")
        get_user_feedback(symptoms, prediction)
    else:
        diagnosis = diagnose(symptoms)
        display_results(diagnosis)
        if diagnosis and diagnosis[0][1] > 0:
            get_user_feedback(symptoms, diagnosis[0][0])
        else:
            print("Unable to diagnose. Please consult a doctor.")

if __name__ == "__main__":
    main()
