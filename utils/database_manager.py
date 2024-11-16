import sqlite3
from datetime import datetime, timedelta

def update_db(risk_level, user_data):
    """
    Updates the appropriate priority database based on the user's risk level.

    Args:
        risk_level (str): Risk level ("Red", "Yellow", "Green").
        user_data (dict): User details (email and phone).
    """
    db_name = f"db/{risk_level.lower()}.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    email = user_data['Email_id']
    phone = user_data['Phone_No']
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if the user already exists in the priority database
    c.execute(f'SELECT * FROM {risk_level.lower()} WHERE email_id = ? OR phone_no = ?', (email, phone))
    result = c.fetchone()

    if result:
        last_chat_time = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S')
        time_limits = {'red': timedelta(minutes=10), 'yellow': timedelta(hours=1), 'green': timedelta(hours=1)}
        if datetime.now() - last_chat_time > time_limits[risk_level.lower()]:
            # Update last_chat_time
            c.execute(f'UPDATE {risk_level.lower()} SET last_chat_time = ? WHERE id = ?', (current_time, result[0]))
    else:
        # Insert a new record
        c.execute(f'INSERT INTO {risk_level.lower()} (email_id, phone_no, last_chat_time) VALUES (?, ?, ?)',
                  (email, phone, current_time))

    conn.commit()
    conn.close()
