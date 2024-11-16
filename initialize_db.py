import sqlite3
import os

# Ensure 'db' directory exists
db_dir = os.path.join(os.path.dirname(__file__), 'db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Initialize users.db
conn = sqlite3.connect(os.path.join(db_dir, 'users.db'))
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email_id TEXT UNIQUE,
    phone_no TEXT UNIQUE,
    password TEXT NOT NULL,
    age INTEGER,
    gender TEXT
)
''')
conn.commit()
conn.close()

# Initialize red.db
conn = sqlite3.connect(os.path.join(db_dir, 'red.db'))
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS red (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id TEXT,
    phone_no TEXT,
    last_chat_time DATETIME
)
''')
conn.commit()
conn.close()

# Initialize yellow.db
conn = sqlite3.connect(os.path.join(db_dir, 'yellow.db'))
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS yellow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id TEXT,
    phone_no TEXT,
    last_chat_time DATETIME
)
''')
conn.commit()
conn.close()

# Initialize green.db
conn = sqlite3.connect(os.path.join(db_dir, 'green.db'))
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS green (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id TEXT,
    phone_no TEXT,
    last_chat_time DATETIME
)
''')
conn.commit()
conn.close()

print("Databases initialized successfully.")
