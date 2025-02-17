import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("meanings.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS meanings (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               word TEXT NOT NULL,
               meaning TEXT NOT NULL
               date_added DATE DEFAULT CURRENT_DATE
               );
""")

# INSERT SAMPLE MEANINGS
sample_data = [("Serendipity", "The occurrence and development of events by chance in a happy or beneficial way."),]
cursor.executemany("INSERT INTO meanings (word, meaning) VALUES (?, ?)", sample_data)

# Commit and close
conn.commit()
conn.close()

print("Database created successfully.")