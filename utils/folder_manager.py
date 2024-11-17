import os
import json



def create_user_folder(phone):
    folder_name = f"data/{phone}"
    if not os.path.exists(folder_name):
        os.makedirs(f"{folder_name}/chat_session")
        os.makedirs(f"{folder_name}/DOCS")
    print(f"Folder created for user with phone number: {phone}")



def save_chat(phone, user_input, ai_response):
    """
    Saves the chat session to the user's chat session folder.

    Args:
        phone (str): User's phone number.
        user_input (str): User's input message.
        ai_response (str): AI-generated response.

    Returns:
        str: Path to the saved chat session file.
    """
    folder_name = f"data/{phone}/chat_session"
    os.makedirs(folder_name, exist_ok=True)

    chat_data = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "user_input": user_input,
        "ai_response": ai_response
    }

    file_path = os.path.join(folder_name, "conversation.json")
    with open(file_path, "w") as file:
        json.dump(chat_data, file)

    return file_path

def save_to_risk_folder(phone, risk_level, user_info, conversation):
    """
    Saves user data and conversation in the corresponding risk-level folder.

    Args:
        phone (str): User's phone number.
        risk_level (str): Risk level ("Red", "Yellow", "Green").
        user_info (dict): User information to save.
        conversation (list): Conversation data to save.
    """
    base_path = "Admin_Data"
    risk_folder = os.path.join(base_path, risk_level)

    # Create the risk-level folder if it doesn't exist
    os.makedirs(risk_folder, exist_ok=True)

    # Create a user-specific folder using the phone number
    user_folder = os.path.join(risk_folder, phone)
    os.makedirs(user_folder, exist_ok=True)

    # Create a chat session subfolder
    chat_session_folder = os.path.join(user_folder, "chat_session")
    os.makedirs(chat_session_folder, exist_ok=True)

    # Save user info
    user_info_path = os.path.join(user_folder, "user_info.json")
    with open(user_info_path, "w") as user_file:
        json.dump(user_info, user_file)

    # Save conversation data
    conversation_file_path = os.path.join(chat_session_folder, "conversation.json")
    with open(conversation_file_path, "w") as conversation_file:
        json.dump(conversation, conversation_file)

    print(f"Data saved for user {phone} under {risk_level} folder.")


import os
import json
from datetime import datetime

def save_chat_to_folder(phone_no, conversation_context, risk_level):
    """
    Saves the chat conversation to a folder based on the detected risk level.

    Args:
        phone_no (str): User's phone number.
        conversation_context (list): The entire conversation context.
        risk_level (str): The detected risk level ("Red", "Yellow", "Green").

    Returns:
        str: Path to the saved chat file.
    """
    # Define the base directory for risk levels
    base_dir = f"data/{risk_level}"
    user_dir = os.path.join(base_dir, phone_no)

    # Ensure the directories exist
    os.makedirs(user_dir, exist_ok=True)

    # Save the chat session with a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    chat_file_path = os.path.join(user_dir, f"chat_{timestamp}.json")

    with open(chat_file_path, "w") as f:
        json.dump({"conversation": conversation_context}, f, indent=4)

    print(f"Chat saved to {chat_file_path}")
    return chat_file_path
