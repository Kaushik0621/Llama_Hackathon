document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("user-input");

    chatForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent default form submission

        const userMessage = userInput.value.trim();
        if (!userMessage) {
            alert("Please enter a message before sending.");
            return;
        }

        // Add user message to the chat
        addMessage(userMessage, "user");
        userInput.value = ""; // Clear input

        // Send the message to the server
        fetch("/chat_result", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `message=${encodeURIComponent(userMessage)}`,
        })
            .then((response) => response.json())
            .then((data) => {
                // Add assistant response to the chat
                addMessage(data.reply, "assistant", true);
            })
            .catch((error) => {
                console.error("Error:", error);
                addMessage("Something went wrong. Please try again.", "assistant");
            });
    });

    function addMessage(content, role, isHTML = false) {
        const messageElement = document.createElement("div");
        messageElement.classList.add(role === "user" ? "user-message" : "assistant-message");

        if (isHTML) {
            messageElement.innerHTML = content; // Render HTML content
        } else {
            messageElement.textContent = content; // Render plain text
        }

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
