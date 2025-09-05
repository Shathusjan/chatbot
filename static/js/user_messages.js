export function appendUserMessage(message) {
  const trimmedMessage = message.trim();
  if (!trimmedMessage) return;

  const chatWindow = document.getElementById("chat_window");

  const msgDiv = document.createElement("div");
  msgDiv.className = "flex justify-end my-1";

  msgDiv.innerHTML = `
    <div class="bg-purple-100 text-purple-800 text-sm px-3 py-2 rounded-lg max-w-xs">
      ${trimmedMessage}
    </div>
  `;

  chatWindow.appendChild(msgDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}