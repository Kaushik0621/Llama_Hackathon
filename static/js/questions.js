let currentStep = 0; // Track the current question step

function submitAnswer(answer) {
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ step: currentStep, answer: answer }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.completed) {
            // If all questions are completed, transition to free chat
            alert("All questions answered! Proceeding to chat...");
            window.location.href = '/chat'; // Redirect to the chat interface
        } else {
            // Update the question and options for the next step
            updateQuestion(data.next_question);
            currentStep++;
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateQuestion(questionData) {
    // Update the question text
    document.getElementById('question').textContent = questionData.question;

    // Update the options
    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = ''; // Clear existing options
    questionData.options.forEach(option => {
        const button = document.createElement('button');
        button.classList.add('btn');
        button.textContent = option.text;
        button.onclick = () => submitAnswer(option.text);
        optionsDiv.appendChild(button);
    });
}

// Initialize with the first question (rendered from the server)
document.addEventListener('DOMContentLoaded', () => {
    const firstQuestion = JSON.parse(document.getElementById('initial-question').textContent);
    updateQuestion(firstQuestion);
});
