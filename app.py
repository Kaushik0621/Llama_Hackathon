from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from utils.user_auth import User, authenticate_user, register_user, get_user_by_id
from utils.folder_manager import create_user_folder
from utils.risk_assessment import assess_risk
from utils.chat_handler import handle_chat
from utils.dietitian_chat import handle_dietitian_chat
from utils.blood_report_explainer import handle_blood_report_query
import os

# Load environment variables
from dotenv import load_dotenv
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
        email_id = request.form.get('email_id')
        phone_no = request.form.get('phone_no')
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']

        # Register the user
        success = register_user(name, email_id, phone_no, password, age, gender)
        if success:
            # Create a single folder for the user
            create_user_folder(email_id, phone_no)
            return redirect(url_for('login'))
        else:
            return "User already exists or error in registration."
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form['password']

        user = authenticate_user(identifier, password)
        if user:
            login_user(user)

            # Handle 'next' parameter to redirect appropriately
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('base'))
        else:
            return "Invalid credentials."
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

        # Pass both email and phone to the function
        assistant_reply = handle_dietitian_chat(user_input, current_user.email_id, current_user.phone_no)
        return jsonify({"reply": assistant_reply})

    return render_template('dietitian.html')


from utils.folder_manager import save_uploaded_document

@app.route('/blood_report_explainer', methods=['GET', 'POST'])
@login_required
def blood_report_explainer():
    if request.method == 'POST':
        user_input = request.form.get("message")
        if user_input:
            # Pass both email and phone to the function
            assistant_reply = handle_blood_report_query(user_input, current_user.email_id, current_user.phone_no)
            return jsonify({"reply": assistant_reply})

    return render_template('blood_report_explainer.html')


# Blood report explainer page template

# Chat Routes
@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    # Define the questions
    questions = [
        {
            "id": "question1",
            "text": "What symptoms are you experiencing right now?",
            "options": [
                "Severe chest pain or difficulty breathing",
                "Uncontrolled bleeding or loss of consciousness",
                "Severe pain (e.g., abdominal, head)",
                "Fever, cough, or mild pain",
                "No significant symptoms, general check-up"
            ]
        },
        {
            "id": "question2",
            "text": "How long have you had these symptoms?",
            "options": [
                "Less than 1 hour",
                "1–24 hours",
                "1–7 days",
                "More than a week"
            ]
        },
        {
            "id": "question3",
            "text": "Are you experiencing any of the following? (Select all that apply)",
            "options": [
                "Dizziness or confusion",
                "Severe weakness or inability to move",
                "Nausea/vomiting that doesn’t stop",
                "Moderate fatigue or discomfort",
                "None of the above"
            ],
            "multi": True
        },
        {
            "id": "question4",
            "text": "Do you have any pre-existing medical conditions?",
            "options": [
                "Heart disease, diabetes, or immunocompromised conditions",
                "Pregnant or recent surgery (past 4 weeks)",
                "None"
            ]
        },
        {
            "id": "question5",
            "text": "Have you had any recent injuries or accidents?",
            "options": [
                "Head injury or severe trauma",
                "Moderate injury or significant pain",
                "Minor cuts, bruises, or sprains",
                "No injuries"
            ]
        }
    ]

    # Initialize session variables if not already set
    if "current_question" not in session or "responses" not in session:
        session["current_question"] = 0
        session["responses"] = {}

    # If all questions are answered, calculate risk and redirect to chat_result
    if session["current_question"] >= len(questions):
        return redirect(url_for("chat_result"))

    # Handle POST request: Save user's response
    if request.method == "POST":
        current_question = session["current_question"]
        question_id = questions[current_question]["id"]

        # Save the response
        if questions[current_question].get("multi"):
            session["responses"][question_id] = request.form.getlist(question_id)
        else:
            session["responses"][question_id] = request.form.get(question_id)

        # Increment the question index
        session["current_question"] += 1

        # Redirect to `/chat_result` if all questions are answered
        if session["current_question"] >= len(questions):
            risk_level, total_score = assess_risk(session["responses"])
            session["risk_level"] = risk_level
            return redirect(url_for("chat_result"))

    # Render the current question
    current_question_index = session["current_question"]
    question = questions[current_question_index]
    return render_template("question.html", question=question)

# Chat result and agent handling
@app.route('/chat_result', methods=['GET', 'POST'])
@login_required
def chat_result():
    risk_level = session.get("risk_level")

    if not risk_level:
        # Redirect to `/chat` if questions are not completed
        return redirect(url_for("chat"))

    if risk_level == "Red":
        return render_template(
            "chat_result.html", 
            risk_level=risk_level, 
            message="You are getting a call now. Immediate assistance is being arranged."
        )

    # Show appropriate chat agent interface
    if request.method == "POST":
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"reply": "User input is missing."})

        user_data = {
            "Email_id": current_user.email_id,
            "Phone_No": current_user.phone_no
        }

        # Call the handle_chat function
        assistant_reply, folder_path = handle_chat(user_input, user_data, risk_level)
        return jsonify({"reply": assistant_reply})

    # Render the chat interface
    return render_template("chat_result.html", risk_level=risk_level)

# Reset Chat
@app.route('/reset_chat', methods=['POST', 'GET'])
@login_required
def reset_chat():
    session.pop("current_question", None)
    session.pop("responses", None)
    session.pop("risk_level", None)
    return redirect(url_for("chat"))

if __name__ == '__main__':
    app.run(debug=True)
