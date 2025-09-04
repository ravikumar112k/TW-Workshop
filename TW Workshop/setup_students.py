# setup_students.py
import sqlite3

conn = sqlite3.connect("catalog.db")
c = conn.cursor()

# Create students table
c.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    enrolled_category TEXT
)
""")

conn.commit()
conn.close()
print("✅ Students table created in catalog.db")
