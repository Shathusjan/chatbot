export function renderOptionButtons(options, handleUserInput) {
    const bottomOptions = document.getElementById('bottom-options'); // use existing div
    bottomOptions.innerHTML = ''; // clear old options

    if (!options) {
        console.warn("⚠️ No options provided to renderOptionButtons");
        return;
    }

    let normalizedOptions = [];

    if (Array.isArray(options)) {
        normalizedOptions = options.map(opt =>
            typeof opt === 'string' ? opt : (opt.label || JSON.stringify(opt))
        );
    } else if (typeof options === 'object') {
        normalizedOptions = Object.values(options);
    }

    normalizedOptions.forEach(option => {
        const btn = document.createElement('button');
        btn.className = 'px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium hover:bg-purple-200 transition';
        btn.textContent = option;
        btn.addEventListener('click', function () {
            bottomOptions.innerHTML = ''; 
            handleUserInput(option);      
        });
        bottomOptions.appendChild(btn);
    });
}

export function clearOptionButtons() {
    const bottomOptions = document.getElementById('bottom-options');
    if (bottomOptions) {
        bottomOptions.innerHTML = '';
    }
}