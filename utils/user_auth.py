import os
import json
from flask_login import UserMixin

class User(UserMixin):
    """
    A user class compatible with Flask-Login.
    """
    def __init__(self, id, name, phone_no, password, age, gender):
        self.id = id
        self.name = name
        self.phone_no = phone_no
        self.password = password
        self.age = age
        self.gender = gender

    def get_id(self):
        """
        Override Flask-Login's `get_id` method to use the user ID (phone number).
        """
        return str(self.id)

def user_exists(phone_no):
    """
    Checks if a user exists by their phone number.

    Args:
        phone_no (str): The user's phone number.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    user_folder = f"data/{phone_no}"
    user_info_path = os.path.join(user_folder, "user_info.json")
    return os.path.exists(user_info_path)

def save_user_to_db(name, phone_no, password, age, gender):
    """
    Saves user information to the database.

    Args:
        name (str): User's name.
        phone_no (str): User's phone number.
        password (str): User's password.
        age (str): User's age.
        gender (str): User's gender.
    """
    user_data = {
        "name": name,
        "phone_no": phone_no,
        "password": password,
        "age": age,
        "gender": gender
    }
    user_folder = f"data/{phone_no}"
    os.makedirs(user_folder, exist_ok=True)
    user_info_path = os.path.join(user_folder, "user_info.json")
    with open(user_info_path, "w") as f:
        json.dump(user_data, f)

def register_user(name, phone_no, password, age, gender):
    """
    Registers a new user.

    Args:
        name (str): User's name.
        phone_no (str): User's phone number.
        password (str): User's password.
        age (str): User's age.
        gender (str): User's gender.

    Returns:
        bool: True if registration was successful, False otherwise.
    """
    if user_exists(phone_no):
        print(f"User with phone number {phone_no} already exists.")
        return False
    save_user_to_db(name, phone_no, password, age, gender)
    print(f"User registered with phone number: {phone_no}")
    return True

def authenticate_user(phone_no, password):
    """
    Authenticates a user by phone number and password.

    Args:
        phone_no (str): The user's phone number.
        password (str): The user's password.

    Returns:
        User: A User object if authentication is successful, None otherwise.
    """
    user_folder = f"data/{phone_no}"
    user_info_path = os.path.join(user_folder, "user_info.json")

    if not os.path.exists(user_info_path):
        print(f"User info file not found for phone number: {phone_no}")
        return None

    with open(user_info_path, "r") as f:
        user_data = json.load(f)

    if user_data.get("password") == password:
        print(f"Authentication successful for phone number: {phone_no}")
        return User(
            id=user_data["phone_no"],
            name=user_data["name"],
            phone_no=user_data["phone_no"],
            password=user_data["password"],
            age=user_data["age"],
            gender=user_data["gender"]
        )
    else:
        print(f"Incorrect password for phone number: {phone_no}")
        return None

def get_user_by_id(user_id):
    """
    Fetches a User object by ID (phone number).

    Args:
        user_id (str): The user's phone number.

    Returns:
        User: A User object if the user exists, None otherwise.
    """
    user_folder = f"data/{user_id}"
    user_info_path = os.path.join(user_folder, "user_info.json")

    if os.path.exists(user_info_path):
        with open(user_info_path, "r") as f:
            user_data = json.load(f)
        return User(
            id=user_data["phone_no"],
            name=user_data["name"],
            phone_no=user_data["phone_no"],
            password=user_data["password"],
            age=user_data["age"],
            gender=user_data["gender"]
        )
    return None
