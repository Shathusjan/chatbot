import { appendUserMessage } from "./user_messages.js";
import { appendBotMessage } from "./bot_messages.js";

document.addEventListener('DOMContentLoaded', function () {
    const chatWindow = document.getElementById('chat_window');
    const inputBox = document.getElementById('chat-input');

    // Send user input to backend and handle response
    window.handleUserInput = function (message) {
        if (!message.trim()) return;
        // Hide the .quick-actions div if present
        const quickActions = document.querySelector('.quick-actions');
        if (quickActions) {
            quickActions.style.display = 'none';
        }
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
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                const data = await response.json().catch(() => ({}));

                if (data && typeof data === "object") {
                    if (data.reply && data.reply.trim() !== "") {
                        appendBotMessage(data.reply);
                    }
                    if (Array.isArray(data.options) && data.options.length > 0) {
                        if (window.OptionButtons && typeof window.OptionButtons.showOptions === "function") {
                            window.OptionButtons.showOptions(data.options, handleUserInput);
                        } else {
                            console.warn("OptionButtons module not loaded or showOptions missing");
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
    }

    // Event listener for Enter key on input
    inputBox.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const msg = inputBox.value;
            handleUserInput(msg);
        }
    });
});