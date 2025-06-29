import sqlite3

conn = sqlite3.connect("hospital.db")
c = conn.cursor()

print("🔍 Patients with Assigned Doctors:\n")

query = """
SELECT 
    patients.patient_id,
    patients.name AS patient_name,
    patients.age,
    patients.disease,
    doctors.name AS doctor_name,
    doctors.specialization
FROM patients
LEFT JOIN doctors ON patients.doctor_id = doctors.doctor_id
"""

for row in c.execute(query):
    print(f"Patient ID: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"Age: {row[2]}")
    print(f"Disease: {row[3]}")
    print(f"Assigned Doctor: {row[4]} ({row[5]})")
    print("-" * 40)

conn.close()
