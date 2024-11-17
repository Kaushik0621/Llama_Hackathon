# LLAMA CARE: GP Llama Receptionist

LLAMA CARE: GP Llama Receptionist is an innovative healthcare web application designed to revolutionize patient triage for General Practitioners (GPs). Using AI-powered chat and voice-based interactions, this solution drastically reduces waiting times, enhances triage accuracy, and ensures timely responses for emergency cases.

---

## 🚀 Key Features

- **Fast Triage**: Cuts waiting times from hours to minutes.
- **AI-Powered Assistance**: Chat or voice interaction to assess emergency levels (Red, Amber, Green).
- **Real-Time Guidance**: Offers actionable recommendations while patients wait.
- **Seamless Integration**: Provides GP receptionists with detailed patient data and triage summaries to improve decision-making.
- **Voice Call Support**: Users can call the AI agent, describe symptoms, and receive triage decisions and waiting times.
- **Critical Case Handling**: Urgent cases are immediately connected to medical professionals for direct assistance.
- **Secure and Personalized AI**: User consent ensures data privacy and personalization.
- **RAG-Based Knowledge Graphs**: Delivers a customized user experience while allowing control over data usage.

---

## 🛠️ Technologies Used

- **GROQ API**: Utilized Llama 3.2 Vision and Llama 3.1 models for AI interactions and actionable solutions.
- **AI Triage System**: Implemented intelligent categorization of cases into Red, Amber, or Green severity levels.
- **Voice and Web Interfaces**: Supports both web-based chatbots and voice interactions via calls.
- **Admin Panel**: Enables administrators to monitor categories and provide tailored solutions.
- **RAG (Retrieval-Augmented Generation)**: Enhances knowledge-based responses for personalized care.

---

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

*(Provide screenshots showcasing the web interface, AI chatbot, admin panel, and triage results.)*

---

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
