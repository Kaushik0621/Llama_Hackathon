import os
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from utils.user_auth import authenticate_user, register_user, get_user_by_id
from utils.folder_manager import create_user_folder
from utils.chat_handler import handle_chat
from utils.dietitian_chat import handle_dietitian_chat
from utils.blood_report_explainer import handle_blood_report_query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")  # Default secret key

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    return render_template('index.html')  # Login and Signup page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        phone_no = request.form.get('phone_no')  # Phone number
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']  # Gender

        # Call the register_user function with all required parameters
        success = register_user(name, phone_no, password, age, gender)
        if success:
            # Create a folder for the user using their phone number
            create_user_folder(phone_no)
            return redirect(url_for('login'))
        else:
            return "User already exists or there was an error in registration."
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_no = request.form.get('identifier')  # Using phone number as identifier
        password = request.form['password']

        # Authenticate the user
        user_data = authenticate_user(phone_no, password)
        if user_data:
            # Create a User object
            user = get_user_by_id(phone_no)
            login_user(user)

            # Redirect to the base page after successful login
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('base'))
        else:
            return "Invalid credentials, please try again."

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Clear session data
    return redirect(url_for('index'))

@app.route('/base')
@login_required
def base():
    return render_template('base.html')  # Base page with "Go to Chat" link

@app.route('/dietitian', methods=['GET', 'POST'])
@login_required
def dietitian():
    if request.method == 'POST':
        user_input = request.form.get("message")
        if not user_input.strip():
            return jsonify({"reply": "Please ask a relevant question about diet."})

        assistant_reply = handle_dietitian_chat(user_input, current_user.phone_no)
        return jsonify({"reply": assistant_reply})

    return render_template('dietitian.html')

@app.route('/blood_report_explainer', methods=['GET', 'POST'])
@login_required
def blood_report_explainer():
    if request.method == 'POST':
        user_input = request.form.get("message")
        if user_input:
            assistant_reply = handle_blood_report_query(user_input, current_user.phone_no)
            return jsonify({"reply": assistant_reply})

    return render_template('blood_report_explainer.html')



@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if "conversation" not in session:
        session["conversation"] = []  # Initialize session for storing the conversation

    if request.method == "POST":
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"reply": "User input is missing."})

        # Append user input to the conversation
        session["conversation"].append({"role": "user", "content": user_input})

        # Simulate assistant reply
        assistant_reply = "Thank you for your message. Let me assist you further."
        session["conversation"].append({"role": "assistant", "content": assistant_reply})

        session.modified = True  # Mark session as modified
        return jsonify({"reply": assistant_reply})

    return render_template("chat_result.html", risk_level=None)



@app.route('/chat_result', methods=['GET', 'POST'])
@login_required
def chat_result():
    risk_level = session.get("risk_level")
    if not risk_level:
        return redirect(url_for("chat"))

    if risk_level == "Red":
        return render_template(
            "chat_result.html", 
            risk_level=risk_level, 
            message="You are getting a call now. Immediate assistance is being arranged."
        )

    if request.method == "POST":
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"reply": "User input is missing."})

        user_data = {"Phone_No": current_user.phone_no}
        assistant_reply, folder_path = handle_chat(user_input, user_data, risk_level)
        return jsonify({"reply": assistant_reply})

    return render_template("chat_result.html", risk_level=risk_level)

@app.route('/reset_chat', methods=['POST', 'GET'])
@login_required
def reset_chat():
    session.pop("risk_level", None)
    return redirect(url_for("chat"))

if __name__ == '__main__':
    app.run(debug=True)
