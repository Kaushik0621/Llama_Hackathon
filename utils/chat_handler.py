import os
import requests
from .folder_manager import save_chat
from .database_manager import update_db

# GROQ API configuration
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize conversation context
conversation_context = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def handle_chat(user_input, user_data, risk_level):
    """
    Handles chat interaction using GROQ API and returns the reply and folder path.

    Args:
        user_input (str): The user's input message.
        user_data (dict): User details (email and phone).
        risk_level (str): The user's risk level ("Red", "Yellow", or "Green").

    Returns:
        tuple: A tuple containing the reply and folder path of the saved chat session.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in the environment variables.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # Define the system message based on risk level
    if risk_level == "Red":
        update_db(risk_level, user_data)  # Update the priority database
        return "You will receive a call soon. Immediate assistance is being arranged.", None
    elif risk_level == "Yellow":
        system_message = "You are a medical professional. Suggest the patient what they need."
    else:  # Green
        system_message = "You are a nurse. Suggest and explain medical reports to the user."

    # Append system message if this is the first interaction
    if len(conversation_context) == 1:
        conversation_context.append({"role": "system", "content": system_message})

    # Validate and add user input
    if not user_input.strip():
        return "Input cannot be empty.", None
    conversation_context.append({"role": "user", "content": user_input.strip()})

    # Build the payload for the API request
    payload = {
        "model": "llama3-8b-8192",  # Replace with a valid model from GROQ documentation
        "messages": conversation_context,
        "temperature": 0.5,
        "max_tokens": 150,
        "top_p": 1,
        "n": 1,
        "stream": False,
    }

    try:
        # Send the POST request to GROQ API
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Parse the API response
        data = response.json()
        assistant_reply = data['choices'][0]['message']['content'].strip()

        # Save the chat session
        folder_path = save_chat(user_data["Email_id"], user_data["Phone_No"], user_input, assistant_reply)

        # Append assistant reply to the conversation context
        conversation_context.append({"role": "assistant", "content": assistant_reply})

        # Update the database with the risk level (only for Yellow and Green)
        if risk_level in ["Yellow", "Green"]:
            update_db(risk_level, user_data)

        return assistant_reply, folder_path

    except requests.exceptions.RequestException as e:
        # Log detailed error information for debugging
        print("API Request Error:", e)
        if e.response is not None:
            print("Response Status Code:", e.response.status_code)
            print("Response Content:", e.response.text)
        return f"Error: {e}", None
