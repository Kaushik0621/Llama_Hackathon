import requests
import json
import time

# Webhook URL (assuming Flask is running locally on port 5001)
webhook_url = "http://localhost:5001/webhook/create_user"
# webhook_url = "https://llama-hackathon-heroku-ac0409d236cb.herokuapp.com/webhook/create_user"


# Sample user data matching the required fields
test_data = {
    "phone_number": "+44113534536222289",
    "patient_name": "Jane Smith",
    "date_of_birth": "March 15, 1985",
    "medical_conditions": "Asthma",
    "summary": "New patient registration with asthma history",
    "risk_level": "yellow"
}

# Set headers for JSON content
headers = {
    'Content-Type': 'application/json'
}

# Add this function to check notifications after webhook
def check_notifications():
    notifications_url = "http://localhost:5001/get_notifications"  # Adjust URL as needed
    # notifications_url = "https://llama-hackathon-heroku-ac0409d236cb.herokuapp.com/get_notifications"
    
    try:
        response = requests.get(notifications_url)
        print("\nChecking notifications:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error checking notifications: {e}")

# Make the POST request
try:
    response = requests.post(
        webhook_url,
        data=json.dumps(test_data),
        headers=headers
    )
    
    # Print webhook response
    print(f"Status Code: {response.status_code}")
    print("Webhook Response:")
    print(json.dumps(response.json(), indent=2))
    
    # Add small delay and check notifications
    print("\nWaiting 1 second for notification processing...")
    time.sleep(1)  # Give server time to process
    check_notifications()
    
except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")