import sqlite3

# Connect or create the database file
conn = sqlite3.connect("patients.db")
c = conn.cursor()

# Drop existing tables if needed (optional but safe)
c.execute("DROP TABLE IF EXISTS patients")
c.execute("DROP TABLE IF EXISTS doctors")

# Create the patients table
c.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        appointment TEXT
    )
""")

# Create the doctors table
c.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        appointment TEXT
    )
""")

conn.commit()
conn.close()

print("Database setup complete.")
