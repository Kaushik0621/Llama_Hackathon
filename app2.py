from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_from_directory
import os
from pathlib import Path
import json
from datetime import datetime
from werkzeug.utils import secure_filename

# Configuration
ADMIN_USERNAME = "ADMIN"
ADMIN_PASSWORD = "Admin@123"
UPLOAD_FOLDER = "Admin_Data"  # Your folder structure

app2 = Flask(__name__)
app2.secret_key = os.getenv("ADMIN_SECRET_KEY", "default_admin_secret_key")

def load_user_data():
    """
    Loads all user data, including chat sessions and uploads.
    """
    data_dir = Path(UPLOAD_FOLDER)
    user_data = []

    red_count = 0
    yellow_count = 0
    green_count = 0
    new_red_count = 0
    new_yellow_count = 0
    new_green_count = 0

    for priority in ["Red", "Yellow", "Green"]:
        priority_dir = data_dir / priority

        if priority_dir.exists():
            user_folders = [folder for folder in priority_dir.iterdir() if folder.is_dir()]
            for user_folder in user_folders:
                user_info = {}
                chat_sessions = []

                # Load user_info.json
                user_info_path = user_folder / "user_info.json"
                if user_info_path.exists():
                    with open(user_info_path, "r") as f:
                        user_info = json.load(f)

                # Load chat session files
                chat_dir = user_folder / "chat_session"
                if chat_dir.exists():
                    for chat_file in chat_dir.glob("*.json"):
                        with open(chat_file, "r") as f:
                            chat_data = json.load(f)
                        chat_sessions.append(chat_data)

                # Count users in each category
                if priority == "Red":
                    red_count += 1
                    if user_info.get('is_new_case', False):
                        new_red_count += 1
                elif priority == "Yellow":
                    yellow_count += 1
                    if user_info.get('is_new_case', False):
                        new_yellow_count += 1
                elif priority == "Green":
                    green_count += 1
                    if user_info.get('is_new_case', False):
                        new_green_count += 1

                # Append user data
                user_data.append({
                    "user_id": user_folder.name,
                    "user_info": user_info,
                    "risk_level": priority,
                    "chats": chat_sessions
                })

    return user_data, red_count, yellow_count, green_count, new_red_count, new_yellow_count, new_green_count

@app2.route('/')
def admin_index():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin_dashboard'))

@app2.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        return "Invalid admin credentials. Please try again."

    return render_template('admin_login.html')

@app2.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    # Get the user data and counts
    user_data, red_count, yellow_count, green_count, new_red_count, new_yellow_count, new_green_count = load_user_data()

    # Get initial notifications only for new cases
    initial_notifications = []
    if new_red_count > 0:
        initial_notifications.append({
            "message": f"You have {new_red_count} new high priority cases requiring attention!",
            "type": "red"
        })
    if new_yellow_count > 0:
        initial_notifications.append({
            "message": f"{new_yellow_count} new cases in medium priority queue",
            "type": "yellow"
        })

    return render_template('admin_dashboard.html', 
                         red_count=red_count, 
                         yellow_count=yellow_count, 
                         green_count=green_count,
                         new_red_count=new_red_count,
                         new_yellow_count=new_yellow_count,
                         new_green_count=new_green_count,
                         initial_notifications=initial_notifications)

@app2.template_filter('format_datetime')
def format_datetime(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%B %d, %Y %I:%M %p")
    except:
        return value

@app2.route('/admin/queue/<queue>')
def admin_queue(queue):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    # Get user data for the specified queue
    user_data = []
    queue_path = Path(UPLOAD_FOLDER) / queue
    if queue_path.exists():
        for user_folder in queue_path.iterdir():
            if user_folder.is_dir():
                user_info_path = user_folder / "user_info.json"
                if user_info_path.exists():
                    with open(user_info_path) as f:
                        user_info = json.load(f)
                        user_data.append({
                            'user_id': user_folder.name,
                            'risk_level': queue,
                            'user_info': user_info
                        })
    
    # Split users into new and existing cases
    new_cases = [user for user in user_data if user['user_info'].get('is_new_case', False)]
    existing_cases = [user for user in user_data if not user['user_info'].get('is_new_case', False)]
    
    # Standardize the data structure for new cases
    standardized_new_cases = []
    for case in new_cases:
        standardized_case = {
            'user_id': case.get('user_id', ''),
            'risk_level': case.get('risk_level', 'N/A'),
            'user_info': {
                'phone_number': case.get('phone_number', 'N/A'),
                'patient_name': case.get('patient_name', 'N/A'),
                'date_of_birth': case.get('date_of_birth', 'N/A'),
                'medical_conditions': case.get('medical_conditions', 'N/A'),
                'summary': case.get('summary', 'N/A'),
                'created_at': case.get('created_at', '1970-01-01T00:00:00')
            }
        }
        standardized_new_cases.append(standardized_case)

    # Helper function for sorting with fallback
    def get_creation_time(user):
        try:
            return -datetime.fromisoformat(user['user_info'].get('created_at', '1970-01-01T00:00:00')).timestamp()
        except (ValueError, TypeError):
            return float('-inf')
    
    # Sort both lists by creation date (newest to oldest)
    standardized_new_cases.sort(key=get_creation_time)
    existing_cases.sort(key=get_creation_time)
    
    return render_template('admin_queue.html', 
                         queue=queue, 
                         new_cases=standardized_new_cases,
                         existing_cases=existing_cases)

@app2.route('/admin/user/<user_id>')
def admin_user_detail(user_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    # Get user data based on user_id
    user_data, _, _, _, _, _, _ = load_user_data()

    # Find the user by user_id
    user_info = next((user for user in user_data if user['user_id'] == user_id), None)

    if not user_info:
        return "User not found.", 404

    return render_template('admin_user_detail.html', user_info=user_info)

@app2.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app2.route('/webhook/create_user', methods=['POST'])
def create_user_webhook():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['phone_number', 'patient_name', 'date_of_birth', 
                      'medical_conditions', 'summary', 'risk_level']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create user directory structure
    risk_level = data['risk_level'].title()
    user_id = secure_filename(data['phone_number'])
    user_path = Path(UPLOAD_FOLDER) / risk_level / user_id
    
    # Create directories if they don't exist
    user_path.mkdir(parents=True, exist_ok=True)
    (user_path / "chat_session").mkdir(exist_ok=True)
    
    # Save user info with new case flag
    user_info = {
        "phone_number": data['phone_number'],
        "patient_name": data['patient_name'],
        "date_of_birth": data['date_of_birth'],
        "medical_conditions": data['medical_conditions'],
        "summary": data['summary'],
        "risk_level": risk_level,
        "created_at": datetime.now().isoformat(),
        "is_new_case": True
    }
    
    with open(user_path / "user_info.json", "w") as f:
        json.dump(user_info, f, indent=2)
    
    response = jsonify({"status": "success"})
    response.headers['X-Check-Notifications'] = 'true'
    return response

@app2.route('/admin/check-notifications')
def check_notifications():
    if not session.get('admin'):
        return jsonify({"error": "Unauthorized"}), 401
    
    # Load user data to check for new notifications
    user_data, red_count, yellow_count, green_count, new_red_count, new_yellow_count, new_green_count = load_user_data()
    
    notifications = []
    
    # Example notification logic - you can modify based on your needs
    if new_red_count > 0:
        notifications.append({
            "message": f"You have {new_red_count} new high priority cases requiring attention!",
            "type": "red"
        })
    if new_yellow_count > 0:
        notifications.append({
            "message": f"{new_yellow_count} new cases in medium priority queue",
            "type": "yellow"
        })
    
    return jsonify(notifications)

if __name__ == '__main__':
    app2.run(port=5001, debug=True)
