# Symptom Checker & Appointment Booking System

This is a **self-learning Symptom Checker web application** built with **Flask**, **Machine Learning**, and **SQLite**.  
It allows patients to:

 Answer symptoms and get disease predictions (ML + rule-based)
 Give feedback to improve the model
 Book appointments with doctors
 Store patient and doctor data securely

---

##  Features

 Hybrid diagnosis: Rule-based + ML model (Naive Bayes)
   Self-learning: Model improves using patient feedback
   User-friendly UI: Pastel colors for a calm experience
   Appointment booking: Stores patient details & assigns doctors
   SQLite database for storing patients and doctors

---

##  Project Structure
symptom_checker_project/
├── app.py # Flask app entry point
├── ml_model.py # ML model training/updating script
├── setup_db.py # Creates SQLite tables
├── patient.db # SQLite database
├── feedback_data.json # Stores user feedback for training
├── templates/ # HTML templates
│ ├── welcome.html
│ ├── index.html
│ ├── result.html
│ ├── thankyou.html
│ ├── book_appointment.html
│ └── appointment_success.html
├── static/ # (Optional) CSS, JS, images
├── requirements.txt # Python dependencies
├── README.md # Project description
├── .gitignore # Files to ignore in Git


