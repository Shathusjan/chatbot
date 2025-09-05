import { appendUserMessage } from "./user_messages.js";
import { appendBotMessage } from "./bot_messages.js";

document.addEventListener('DOMContentLoaded', function () {
    const chatWindow = document.getElementById('chat_window');
    const inputBox = document.getElementById('chat-input');

    // Load saved conversation from sessionStorage
    const savedChat = sessionStorage.getItem("chatHistory");
    if (savedChat) {
        const history = JSON.parse(savedChat);
        history.forEach(msg => {
            if (msg.sender === "user") {
                appendUserMessage(msg.text);
            } else {
                appendBotMessage(msg.text, msg.options, handleUserInput);
            }
        });
    }

    // Helper: save chat state
    function saveMessage(sender, text, options = null) {
        let history = JSON.parse(sessionStorage.getItem("chatHistory") || "[]");
        history.push({ sender, text, options });
        sessionStorage.setItem("chatHistory", JSON.stringify(history));
    }

    // Send user input to backend and handle response
    window.handleUserInput = function (message) {
        if (!message.trim()) return;

        const quickActions = document.querySelector('.quick-actions');
        if (quickActions) quickActions.style.display = 'none';

        appendUserMessage(message);
        saveMessage("user", message);
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
                        saveMessage("bot", data.reply, data.options || null);
                    }
                }
            } catch (err) {
                console.error("Chat processing error:", err);
                appendBotMessage("Sorry, there was an error.");
                saveMessage("bot", "Sorry, there was an error.");
            }
        })
        .catch(err => {
            console.error("Fetch error:", err);
            appendBotMessage("Sorry, there was an error.");
            saveMessage("bot", "Sorry, there was an error.");
        })
        .finally(() => {
            inputBox.disabled = false;
            inputBox.focus();
        });
    };

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