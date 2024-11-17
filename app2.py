from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_from_directory
import os
import json
from pathlib import Path

# Configuration
ADMIN_USERNAME = "ADMIN"
ADMIN_PASSWORD = "Admin@123"
UPLOAD_FOLDER = "data"

app2 = Flask(__name__)
app2.secret_key = os.getenv("ADMIN_SECRET_KEY", "default_admin_secret_key")

def load_user_data():
    """
    Loads all user data, including chat sessions and uploads.
    """
    data_dir = Path(UPLOAD_FOLDER)
    user_folders = [folder for folder in data_dir.iterdir() if folder.is_dir()]
    
    user_data = []
    for user_folder in user_folders:
        user_chats = []
        user_docs = []
        risk_level = None

        # Load chat session files
        chat_dir = user_folder / "chat_session"
        if chat_dir.exists():
            for chat_file in chat_dir.glob("*.json"):
                with open(chat_file, "r") as f:
                    chat_data = json.load(f)
                user_chats.append(chat_data)

        # Load uploaded documents
        docs_dir = user_folder / "DOCS"
        if docs_dir.exists():
            user_docs = [str(doc) for doc in docs_dir.glob("*")]

        # Determine risk level from the user's folder name or data (dummy logic)
        if "red" in user_folder.name.lower():
            risk_level = "Red"
        elif "yellow" in user_folder.name.lower():
            risk_level = "Yellow"
        elif "green" in user_folder.name.lower():
            risk_level = "Green"

        user_data.append({
            "user_id": user_folder.name,
            "chats": user_chats,
            "docs": user_docs,
            "risk_level": risk_level
        })

    return user_data

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
    return render_template('admin_dashboard.html')

@app2.route('/admin/users')
def admin_users():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    user_data = load_user_data()
    return render_template('admin_users.html', user_data=user_data)

@app2.route('/admin/queue/<queue>')
def admin_queue(queue):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    user_data = load_user_data()
    filtered_users = [user for user in user_data if user['risk_level'] == queue.capitalize()]
    return render_template('admin_queue.html', queue=queue.capitalize(), users=filtered_users)

@app2.route('/admin/user/<user_id>')
def admin_user_detail(user_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    user_data = load_user_data()
    user_info = next((user for user in user_data if user['user_id'] == user_id), None)

    if not user_info:
        return "User not found.", 404

    return render_template('admin_user_detail.html', user_info=user_info)

@app2.route('/admin/download/<path:filename>')
def admin_download(filename):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    file_path = Path(filename)
    if file_path.exists():
        return send_from_directory(file_path.parent, file_path.name, as_attachment=True)

    return "File not found.", 404

@app2.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app2.run(port=5001, debug=True)