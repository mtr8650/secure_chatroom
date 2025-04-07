document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");

    // Function to display a message in the chat box
    function displayMessage(text, isUser = false) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");
        if (isUser) {
            messageElement.classList.add("user-message");
        }
        messageElement.textContent = text;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message
    }

    // Function to send a message to the FastAPI backend
    async function sendMessage() {
        const text = messageInput.value.trim();
        if (text === "") return;

        displayMessage(text, true); // Show user message
        messageInput.value = ""; // Clear input field

        try {
            const response = await fetch("http://127.0.0.1:8000/send", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            // If the user requests "history", display chat history
            if (data.history) {
                chatBox.innerHTML = ""; // Clear chat box
                data.history.forEach(msg => {
                    displayMessage(`${msg.text} (${msg.timestamp})`);
                });
            } else {
                displayMessage(data.message); // Show server response
            }
        } catch (error) {
            console.error("Error sending message:", error);
            displayMessage("⚠️ Error: Could not connect to the server.");
        }
    }

    // Send message when the send button is clicked
    sendButton.addEventListener("click", sendMessage);

    // Send message when the user presses Enter
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});

