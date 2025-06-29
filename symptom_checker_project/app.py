from flask import Flask, render_template, request, redirect, session
import joblib
import json
import os
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session tracking

# Load ML model and encoder
model = joblib.load("model.pkl")
encoder = joblib.load("mlb.pkl")
all_symptoms = encoder.classes_.tolist()

FEEDBACK_FILE = "feedback_data.json"
DB_FILE = "hospital.db"


def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "patients.db")
    print("➡️ Using database at:", db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def welcome():
    return render_template("welcome.html")

# ---------- NEW: Patient login ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Get a random doctor
        cursor.execute("SELECT doctor_id FROM doctors")
        doctor_ids = [row[0] for row in cursor.fetchall()]
        doctor_id = random.choice(doctor_ids) if doctor_ids else None

        # Store patient info
        cursor.execute("INSERT INTO patients (name, age, doctor_id) VALUES (?, ?, ?)", (name, age, doctor_id))
        conn.commit()
        session["patient_id"] = cursor.lastrowid  # store patient id in session
        conn.close()

        return redirect("/symptoms")

    return render_template("login.html")

# ---------- SYMPTOM CHECKER ----------
@app.route("/symptoms")
def home():
    return render_template("index.html", symptoms=all_symptoms)

@app.route("/predict", methods=["POST"])
def predict():
    name = session.get("patient_name")
    age = session.get("patient_age")
    selected_symptoms = request.form.getlist("symptoms")
    prediction = model.predict(encoder.transform([selected_symptoms]))[0]

    # Insert into DB
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, disease, appointment)
        VALUES (?, ?, ?, ?)
    """, (name, age, prediction, 'yes'))
    conn.commit()
    conn.close()

    return render_template("result.html", prediction=prediction, symptoms=selected_symptoms)

@app.route("/appointment")
def appointment():
    return render_template("book_appointment.html")



    return render_tem@app.route("/book_appointment", methods=["GET", "POST"])
@app.route("/appointment")
def appointment_form():
    return render_template("appointment_form.html")

@app.route("/book_appointment", methods=["GET", "POST"])
def book_appointment():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        appointment_time = request.form.get("appointment")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patients (name, age, appointment) VALUES (?, ?, ?)",
            (name, age, appointment_time)
        )
        conn.commit()
        conn.close()

        # Show dedicated appointment success page
        return render_template("appointment_success.html")

    return render_template("appointment_form.html")


# ---------- USER FEEDBACK ----------
@app.route("/feedback", methods=["POST"])
def feedback():
    feedback_response = request.form.get("feedback")
    prediction = request.form.get("prediction")
    symptoms = request.form.getlist("symptoms")

    entry = {
        "symptoms": symptoms,
        "predicted_disease": prediction,
        "user_feedback": feedback_response
    }

    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w") as f:
            json.dump([entry], f, indent=2)
    else:
        with open(FEEDBACK_FILE, "r+") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)

    return render_template("thankyou.html")
@app.route("/symptoms", methods=["GET", "POST"])
def symptoms():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")

        if not name or not age:
            return " Name and age are required!", 400  # Graceful error

        # Save patient info in session or DB
        session["patient_name"] = name
        session["patient_age"] = age

    return render_template("index.html", symptoms=all_symptoms)

if __name__ == "__main__":
    app.run(debug=True)
