# setup_db.py
import sqlite3

conn = sqlite3.connect("catalog.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    title TEXT,
    video_url TEXT
)
""")

conn.commit()
conn.close()
print("✅ catalog.db initialized with videos table.")
