from utils.folder_manager import save_chat
from datetime import datetime
import os
import requests

# GROQ API configuration
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize conversation context
conversation_context = [
    {
        "role": "system",
        "content": "You are a knowledgeable dietitian. Answer only diet-related questions. If a question is unrelated to diet, respond with: 'I specialize in diet-related queries. Please ask relevant questions.'"
    }
]
def handle_dietitian_chat(user_input, user_email, user_phone):
    """
    Handles the dietitian chat interaction and saves the session.

    Args:
        user_input (str): The user's input message.
        user_email (str): The user's email for personalization or saving context.
        user_phone (str): The user's phone number for folder management.

    Returns:
        str: The LLM's response to the user's query.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in the environment variables.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # Validate and add user input to the conversation context
    if not user_input.strip():
        return "Please ask a valid question related to your diet."

    conversation_context.append({"role": "user", "content": user_input.strip()})

    # Build the payload for the API request
    payload = {
        "model": "llama3-8b-8192",  # Replace with the correct model
        "messages": conversation_context,
        "temperature": 0.5,
        "max_tokens": 200,
        "top_p": 1,
        "n": 1,
        "stream": False,
    }

    try:
        # Send the POST request to the GROQ API
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Parse the API response
        data = response.json()
        assistant_reply = data['choices'][0]['message']['content'].strip()

        # Append the assistant's response to the context
        conversation_context.append({"role": "assistant", "content": assistant_reply})

        # Save the chat session
        save_chat(user_email, user_phone, user_input, assistant_reply)

        return assistant_reply

    except requests.exceptions.RequestException as e:
        # Log detailed error information for debugging
        print("API Request Error:", e)
        if e.response is not None:
            print("Response Status Code:", e.response.status_code)
            print("Response Content:", e.response.text)
        return "There was an error processing your request. Please try again later."
