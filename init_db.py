import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    email TEXT NOT NULL,

    rating INTEGER,

    comments TEXT,

    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

conn.close()

print("Database table created successfully!")