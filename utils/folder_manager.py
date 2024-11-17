import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

def create_user_folder(email, phone):
    """
    Creates a folder for a user with the format "email_phone".

    Args:
        email (str): User's email.
        phone (str): User's phone number.
    """
    folder_name = f"data/{email}_{phone}"
    if not os.path.exists(folder_name):
        os.makedirs(f"{folder_name}/chat_session")
        os.makedirs(f"{folder_name}/DOCS")


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
        create_user_folder(email, phone)

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


def save_uploaded_document(email, phone, file):
    """
    Saves an uploaded document to the user's DOCS folder.

    Args:
        email (str): User's email ID.
        phone (str): User's phone number.
        file (FileStorage): The uploaded file.

    Returns:
        str: Path to the saved document or an error message.
    """
    folder_name = f"data/{email}_{phone}/DOCS"
    if not os.path.exists(folder_name):
        create_user_folder(email, phone)

    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'pdf', 'png', 'jpg', 'jpeg'}:
        filename = secure_filename(file.filename)
        file_path = os.path.join(folder_name, filename)
        file.save(file_path)
        return file_path, None
    else:
        return None, "Unsupported file format. Please upload PDF, PNG, JPG, or JPEG files."
