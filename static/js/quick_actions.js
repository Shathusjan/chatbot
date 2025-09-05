document.addEventListener("DOMContentLoaded", () => {
  const quickActions = [
    "Get a quote",
    "Cake types",
    "Flavour",
    "Size and servings",
    "Price",
    "Special offers",
    "Custom design"
  ];

  const container = document.querySelector(".quick-actions");
  container.className = "quick-actions flex gap-2 overflow-x-auto whitespace-nowrap px-4 py-2 bg-gray-50";
  container.style.scrollbarWidth = "none"; // Firefox
  container.style.msOverflowStyle = "none"; // IE/Edge
  container.style.overflowY = "hidden"; 
  container.addEventListener("wheel", (e) => {
    if (e.deltaY !== 0) {
      e.preventDefault();
      container.scrollLeft += e.deltaY;
    }
  });

  quickActions.forEach(action => {
    const btn = document.createElement("button");
    btn.textContent = action;
    btn.className = "bg-purple-100 text-purple-700 px-3 py-2 rounded-full hover:bg-purple-200 text-sm whitespace-nowrap";
    btn.onclick = () => handleUserInput(action); // re-use your existing function
    container.appendChild(btn);
  });

  const style = document.createElement("style");
  style.textContent = `
    .quick-actions::-webkit-scrollbar {
      display: none;
    }
  `;
  document.head.appendChild(style);
});