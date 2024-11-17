import os
import requests
from .folder_manager import save_to_risk_folder
from .folder_manager import save_chat_to_folder


# GROQ API configuration
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize conversation context
conversation_context = [
    {"role": "system", "content": "You are a medical professional. Assist the user with their medical queries."}
]
def handle_chat(user_input, user_data):
    """
    Handles chat interaction using the LLM and saves data under the risk level folder.

    Args:
        user_input (str): The user's input message.
        user_data (dict): User's details.

    Returns:
        tuple: A tuple containing the assistant reply and the folder path.
    """
    # Append user input to the conversation context
    conversation_context.append({"role": "user", "content": user_input})

    # Simulate LLM response
    assistant_reply = "Thank you for your message. Let me assist you further."
    conversation_context.append({"role": "assistant", "content": assistant_reply})

    # Detect risk level
    risk_level = detect_risk_level(conversation_context)
    if risk_level not in ["Red", "Yellow", "Green"]:
        raise ValueError(f"Unexpected risk level: {risk_level}")

    # Save chat to folder based on risk level
    folder_path = save_chat_to_folder(user_data["Phone_No"], conversation_context, risk_level)
    print(f"Data saved for user {user_data['Phone_No']} under {risk_level} folder.")

    return assistant_reply, folder_path


def detect_risk_level(conversation_context):
    """
    Analyzes the conversation context to detect the risk level.

    Args:
        conversation_context (list): List of messages exchanged in the chat.

    Returns:
        str: Detected risk level ("Red", "Yellow", "Green").
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a medical expert. Assess the severity of the situation."},
            {"role": "user", "content": f"Analyze this conversation: {conversation_context}. What is the risk level (Red, Yellow, Green)?"}
        ],
        "temperature": 0,
        "max_tokens": 50,
        "top_p": 1,
        "n": 1,
        "stream": False,
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        raw_risk_level = data['choices'][0]['message']['content'].strip()

        # Extract only the risk level from the response
        if "Red" in raw_risk_level:
            return "Red"
        elif "Yellow" in raw_risk_level:
            return "Yellow"
        elif "Green" in raw_risk_level:
            return "Green"
        else:
            raise ValueError(f"Unexpected risk level: {raw_risk_level}")

    except requests.exceptions.RequestException as e:
        print("Risk Detection API Request Error:", e)
        return "Unknown"
