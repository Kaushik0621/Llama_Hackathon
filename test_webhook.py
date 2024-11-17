import requests
import json

# Webhook URL (assuming Flask is running locally on port 5001)
webhook_url = "http://localhost:5001/webhook/create_user"

# Sample user data matching the required fields
test_data = {
    "phone_number": "+44123456789",
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

# Make the POST request
try:
    response = requests.post(
        webhook_url,
        data=json.dumps(test_data),
        headers=headers
    )
    
    # Print response
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    
except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")