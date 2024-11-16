import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Replace with your actual Groq API key from the .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

def send_json_to_groq(json_file_path):
    """
    Send a JSON file to the Groq API and return the assistant's response as a single word.
    """
    # Check if API key is available
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is not set. Please check your .env file."

    # Load the JSON content
    try:
        with open(json_file_path, 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        return "Error: JSON file not found."
    except json.JSONDecodeError:
        return "Error: Invalid JSON format."

    # Prepare the prompt
    prompt = """
    You are a medical expert. Based on the following JSON content, return only one word:
    - 'RED' if it is a severe condition.
    - 'YELLOW' if it is not critical but should be handled within 2-3 hours.
    - 'GREEN' if it is not critical at all.

    JSON content:
    {}
    Only return one word: 'RED', 'YELLOW', or 'GREEN'. Do not add any explanation or context.
    """.format(json.dumps(user_data, indent=2))

    # Set up the payload and headers
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama3-8b-8192",  # Specify the model you want to use
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": prompt}],
        "temperature": 0.0,  # Use deterministic response
        "max_tokens": 10,   # Limit tokens to ensure concise response
        "top_p": 1,
        "n": 1,
        "stream": False,
    }

    # Make the request to the Groq API
    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Extract the assistant's reply
        assistant_reply = data['choices'][0]['message']['content'].strip()
        return assistant_reply
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Path to your test JSON file
    json_file_path = "test.json"
    response = send_json_to_groq(json_file_path)
    print(f"LLM Response: {response}")
