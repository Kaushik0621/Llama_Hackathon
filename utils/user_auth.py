from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, email_id, phone_no, password, age, gender):
        self.id = id
        self.name = name
        self.email_id = email_id
        self.phone_no = phone_no
        self.password = password
        self.age = age
        self.gender = gender

def get_user_by_id(user_id):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return User(*result)
    return None

def get_user_by_identifier(identifier):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email_id = ? OR phone_no = ?', (identifier, identifier))
    result = c.fetchone()
    conn.close()
    if result:
        return User(*result)
    return None

def authenticate_user(identifier, password):
    user = get_user_by_identifier(identifier)
    if user and check_password_hash(user.password, password):
        return user
    return None

def register_user(name, email_id, phone_no, password, age, gender):
    hashed_password = generate_password_hash(password)
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (name, email_id, phone_no, password, age, gender) VALUES (?, ?, ?, ?, ?, ?)',
                  (name, email_id, phone_no, hashed_password, age, gender))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
