function showTyping() {
      const chatWindow = document.getElementById('chat_window');
      // Check if the typing indicator already exists
      if (!chatWindow.querySelector('.typing-indicator-scripted')) {
        // Create typing indicator div with Tailwind-compatible animation classes
        const typingDiv = document.createElement('div');
        typingDiv.className = 'flex items-start gap-2 typing-indicator typing-indicator-scripted';
        // Inner HTML includes animated dots styled with Tailwind CSS classes
        typingDiv.innerHTML = `
          <div class="w-8 h-8 bg-purple-600 text-white flex items-center justify-center rounded-full">🤖</div>
          <div class="flex gap-1">
            <span class="w-2 h-2 bg-purple-600 rounded-full animate-bounce animation-delay-200"></span>
            <span class="w-2 h-2 bg-purple-600 rounded-full animate-bounce animation-delay-400"></span>
            <span class="w-2 h-2 bg-purple-600 rounded-full animate-bounce animation-delay-600"></span>
          </div>
        `;
        chatWindow.appendChild(typingDiv);
        // Scroll to bottom if needed
        chatWindow.scrollTop = chatWindow.scrollHeight;
      }
    }

    function hideTyping() {
      const chatWindow = document.getElementById('chat_window');
      const typingDiv = chatWindow.querySelector('.typing-indicator-scripted');
      if (typingDiv) {
        chatWindow.removeChild(typingDiv);
      }
    }

    function appendBotMessage(message) {
      const chatWindow = document.getElementById('chat_window');
      const messageDiv = document.createElement('div');
      messageDiv.className = 'bot-message flex items-start gap-2';
      messageDiv.innerHTML = `
        <div class="w-8 h-8 bg-purple-600 text-white flex items-center justify-center rounded-full">🤖</div>
        <div class="bg-purple-100 text-purple-900 p-2 rounded-lg max-w-xs">${message}</div>
      `;
      chatWindow.appendChild(messageDiv);
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    document.addEventListener('DOMContentLoaded', () => {
      showTyping();
      setTimeout(() => {
        hideTyping();
        appendBotMessage("👋 Hi there! How can I help you today?");
      }, 2000);
    });
