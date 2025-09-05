import { appendUserMessage } from "./user_messages.js";
import { appendBotMessage } from "./bot_messages.js";
import sessionManager from "./session_manager.js";

document.addEventListener('DOMContentLoaded', function () {
    const chatWindow = document.getElementById('chat_window');
    const inputBox = document.getElementById('chat-input');

    // Send user input to backend and handle response
    window.handleUserInput = function (message) {
        if (!message.trim()) return;

        if (message.toLowerCase().includes("quote")) {
            sessionManager.initializeSession("quotation");
        }

        const quickActions = document.querySelector('.quick-actions');
        if (quickActions) quickActions.style.display = 'none';

        appendUserMessage(message);
        inputBox.value = '';
        inputBox.disabled = true;

        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        })
        .then(async response => {
            try {
                if (!response.ok) throw new Error("Network response was not ok");

                const data = await response.json().catch(() => ({}));
                if (data && typeof data === "object") {
                    if (data.reply && data.reply.trim() !== "") {
                        appendBotMessage(data.reply, data.options, handleUserInput);
                        if (sessionManager.isFeatureActive("quotation")) {
                            sessionManager.setStep(data.reply);
                        }
                    }
                }
            } catch (err) {
                console.error("Chat processing error:", err);
                appendBotMessage("Sorry, there was an error.");
            }
        })
        .catch(err => {
            console.error("Fetch error:", err);
            appendBotMessage("Sorry, there was an error.");
        })
        .finally(() => {
            inputBox.disabled = false;
            inputBox.focus();
        });
    };

    // Load saved session and show placeholder if quotation active
    const session = sessionManager.loadSession();
    if (sessionManager.isFeatureActive("quotation")) {
    appendBotMessage(
        "You have an unfinished quotation. Do you want to continue?",
        ["Resume", "Start Over"],
        (choice) => {
            if (choice === "Resume") {
                appendBotMessage("Okay, resuming your quotation...");
                // continue quotation flow...
            } else {
                sessionManager.clearSession();
                appendBotMessage("No problem, let's start fresh!");
            }
        }
    );
}

    // Event listener for Enter key
    inputBox.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const msg = inputBox.value;
            handleUserInput(msg);
        }
    });

    // Helper: reset session if needed (you can call this after quote is completed)
    window.resetChat = function () {
        sessionStorage.removeItem("chatHistory");
        chatWindow.innerHTML = "";
    };
});