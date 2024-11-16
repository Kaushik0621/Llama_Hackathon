import os
import json
from datetime import datetime

def create_user_folder(identifier):
    """
    Creates a folder for a user with their email and phone number.

    Args:
        identifier (str): The user's identifier (email + phone number).
    """
    folder_name = f"data/{identifier}"
    if not os.path.exists(folder_name):
        os.makedirs(f"{folder_name}/chat_session")


def save_chat(email, phone, user_input, ai_response):
    """
    Saves the chat session to the user's chat session folder.

    Args:
        email (str): User's email ID.
        phone (str): User's phone number.
        user_input (str): User's input message.
        ai_response (str): AI-generated response.

    Returns:
        str: Path to the saved chat session file.
    """
    folder_name = f"data/{email}_{phone}"
    if not os.path.exists(folder_name):
        create_user_folder(f"{email}_{phone}")

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    chat_file_path = f"{folder_name}/chat_session/{timestamp}.json"

    chat_data = {
        "timestamp": timestamp,
        "user_input": user_input,
        "ai_response": ai_response
    }

    with open(chat_file_path, 'w') as chat_file:
        json.dump(chat_data, chat_file)

    return chat_file_path
