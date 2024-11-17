from utils.folder_manager import save_chat
from datetime import datetime
import os
import requests

BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def handle_blood_report_query(user_input, user_email, user_phone):
    """
    Handles blood report queries and saves the session.

    Args:
        user_input (str): The user's query.
        user_email (str): The user's email.
        user_phone (str): The user's phone number.

    Returns:
        str: The LLM's response to the query.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in the environment variables.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert in medical blood report analysis. Provide detailed explanations of blood test parameters in simple terms for non-medical users."
            },
            {"role": "user", "content": user_input.strip()},
        ],
        "temperature": 0.5,
        "max_tokens": 200,
        "top_p": 1,
        "n": 1,
        "stream": False,
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        assistant_reply = data['choices'][0]['message']['content'].strip()

        # Save the chat session
        save_chat(user_email, user_phone, user_input, assistant_reply)

        return assistant_reply

    except Exception as e:
        print("Error in Groq LLM:", e)
        return "There was an error processing your query. Please try again later."
