import sqlite3

videos = [
    ("AI", "Artificial Intelligence Fundamentals", "https://www.youtube.com/watch?v=ad79nYk2keg"),
    ("Python", "Python for Data & Apps", "https://www.youtube.com/watch?v=Y8Tko2YC5hA"),
    ("Data Science", "Intro to Data Science", "https://www.youtube.com/watch?v=JL_grPUnXzY"),
    ("Machine Learning", "Machine Learning Essentials", "https://www.youtube.com/watch?v=gmvvaobm7eQ"),
    ("Databases", "Introduction to database", "https://www.youtube.com/watch?v=6Iu45VZGQDk"),
]

conn = sqlite3.connect("catalog.db")
c = conn.cursor()
c.executemany("INSERT INTO videos (category, title, video_url) VALUES (?, ?, ?)", videos)
conn.commit()
conn.close()

print("✅ Sample videos inserted into catalog.db")
