export function appendBotMessage(message, options) {
  const chatWindow = document.getElementById("chat_window");

  const sanitizedMessage = message.trim();

  const msgDiv = document.createElement("div");
  msgDiv.className = "flex flex-col items-start my-1";

  // Split by line breaks
  const lines = sanitizedMessage.split(/\r?\n/);

  // Separate normal lines and bullet lines
  let htmlContent = "";
  let listOpen = false;

  lines.forEach(line => {
    const trimmedLine = line.trim();

    if (/^[-•]\s+/.test(trimmedLine)) {
      // Line is a bullet item
      if (!listOpen) {
        htmlContent += "<ul class='list-disc list-inside text-sm m-0 p-0' >";
        listOpen = true;
      }
      htmlContent += `<li class="text-sm">${trimmedLine.replace(/^[-•]\s+/, '')}</li>`;
    } else {
      // Close list if we were inside one
      if (listOpen) {
        htmlContent += "</ul>";
        listOpen = false;
      }
      if (trimmedLine.length > 0) {
        htmlContent += `<p class="my-1 text-sm ">${trimmedLine}</p>`;
      }
    }
  });

  if (listOpen) {
    htmlContent += "</ul>"; // Close any open list
  }

  msgDiv.innerHTML = `
    <div class="flex items-center">
      <div class="w-8 h-8 bg-purple-600 text-white flex items-center justify-center rounded-full">🤖</div>
      <div class="bg-purple-200 text-purple-900 text-sm px-3 py-2 rounded-lg max-w-xs ml-2">
        ${htmlContent}
      </div>
    </div>
  `;

  // Add option buttons (if any)
  if (options && Array.isArray(options) && options.length > 0) {
    const buttonsContainer = document.createElement("div");
    buttonsContainer.className = "mt-2 flex flex-wrap gap-2";
    

    options.forEach(option => {
      const button = document.createElement("button");
      button.className = "px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium hover:bg-purple-200 transition";
      button.textContent = option;
      button.onclick = () => handleUserInput(option);
      buttonsContainer.appendChild(button);
    });

    msgDiv.appendChild(buttonsContainer);
  }

  chatWindow.appendChild(msgDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}