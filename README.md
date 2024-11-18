# LLAMA CARE: GP Llama Receptionist
<img width="757" alt="Screenshot 2024-11-17 at 12 03 58 PM" src="https://github.com/user-attachments/assets/6c2c85c9-b316-4b80-9a5a-62b8aa3b4268">
<br/>LLAMA CARE: GP Llama Receptionist is an innovative healthcare web application designed to revolutionize patient triage for General Practitioners (GPs). Using AI-powered chat and voice-based interactions, this solution drastically reduces waiting times, enhances triage accuracy, and ensures timely responses for emergency cases.

---

<img width="1421" alt="Screenshot 2024-11-17 at 12 04 19 PM" src="https://github.com/user-attachments/assets/a336d748-e64b-4b3a-81ab-01129d1f5cb6">


## 🚀 Key Features

- **Fast Triage**: Cuts waiting times from hours to minutes.
- **AI-Powered Assistance**: Chat or voice interaction to assess emergency levels (Red, Amber, Green).
- **Real-Time Guidance**: Offers actionable recommendations while patients wait.
- **Seamless Integration**: Provides GP receptionists with detailed patient data and triage summaries to improve decision-making.
- **Voice Call Support**: Users can call the AI agent, describe symptoms, and receive triage decisions and waiting times.
- **Critical Case Handling**: Urgent cases are immediately connected to medical professionals for direct assistance.
- **Secure and Personalized AI**: User consent ensures data privacy and personalization.
- **RAG-Based Knowledge Graphs**: Delivers a customized user experience while allowing control over data usage.
<img width="628" alt="Screenshot 2024-11-17 at 12 05 43 PM" src="https://github.com/user-attachments/assets/28b6cfe7-2e18-41b5-ab9a-6cf273dd97a8">

---


## 🛠️ Technologies Used

- **GROQ API**: Utilized Llama 3.2 Vision and Llama 3.1 models for AI interactions and actionable solutions.
- **AI Triage System**: Implemented intelligent categorization of cases into Red, Amber, or Green severity levels.
- **Voice and Web Interfaces**: Supports both web-based chatbots and voice interactions via calls.
- **Admin Panel**: Enables administrators to monitor categories and provide tailored solutions.
- **RAG (Retrieval-Augmented Generation)**: Enhances knowledge-based responses for personalized care.

---
<img width="1423" alt="Screenshot 2024-11-17 at 12 06 09 PM" src="https://github.com/user-attachments/assets/d2fb51c2-0129-4595-9746-86c8e6b0b226">
<img width="1429" alt="Screenshot 2024-11-17 at 12 09 12 PM" src="https://github.com/user-attachments/assets/47bc5f6d-36d4-4a83-ac6b-b316671ad81d">

## 🔒 Security & Privacy

- **User Consent**: All user data is processed securely with explicit consent.
- **Personalization**: AI chatbots use the provided data to offer personalized solutions while ensuring privacy.
- **Data Control**: Users maintain control over their data usage preferences.

---

## How It Works

1. **User Interaction**: The user can interact via chat or make a voice call to the AI agent.
2. **Symptom Assessment**: AI listens to the user’s symptoms and descriptions.
3. **Triage Categorization**: The condition is classified as Red (Critical), Amber (Moderate), or Green (Non-Critical).
4. **Response & Recommendations**: The user is provided with waiting times or directly connected to a medical professional if the condition is critical.
5. **Admin Dashboard**: GPs and receptionists access categorized data and triage summaries to make informed decisions.

---

## 🌟 Benefits

- Improved accessibility and efficiency in healthcare services.
- Reduced waiting times for patients.
- Enhanced communication between patients and GP receptionists.
- Immediate escalation for critical cases.

---

## 🖼️ Screenshots
<img width="1423" alt="Screenshot 2024-11-17 at 12 06 09 PM" src="https://github.com/user-attachments/assets/998298fe-0336-4104-ad18-cb09e77e22d0">
<img width="1429" alt="Screenshot 2024-11-17 at 12 06 58 PM" src="https://github.com/user-attachments/assets/71f5b8ab-b7bd-48cb-86be-f21af4fa7ec4">



## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Flask
- GROQ API Key
- Dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/llama-care.git
2. cd llama-care
3. Set up your GROQ API key:
Create a .env file in the project root directory and add your GROQ API key:

GROQ_API_KEY=your_groq_api_key_here
4. To run the Web Inter face for the User(as a Patient)
python3 app.py

5. If you an Admin, who want to check the records.. 
python3 app2.py
ID = ADMIN
Password = Admin@123
<img width="1423" alt="Screenshot 2024-11-17 at 12 07 13 PM" src="https://github.com/user-attachments/assets/9008c70f-e230-4101-8814-3f65509e77d4">
<img width="1433" alt="Screenshot 2024-11-17 at 12 07 28 PM" src="https://github.com/user-attachments/assets/183c81dc-cb88-4be6-973f-e39de669f599">

### Youtube Video
<br/>
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/mbcKFoVQ0EI&t=1s/0.jpg)](https://www.youtube.com/watch?v=mbcKFoVQ0EI&t=1s)

