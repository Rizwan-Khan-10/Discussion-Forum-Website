const notifications = [
    {
        icon: 'R',
        color: 'blue',
        message: 'You have a new reply on your post "Discussion Topic 1".',
        time: '5 minutes ago'
    },
    {
        icon: 'M',
        color: 'green',
        message: 'You were mentioned in "Discussion Topic 2".',
        time: '15 minutes ago'
    },
    {
        icon: 'N',
        color: 'yellow',
        message: 'New discussion available in the forum.',
        time: '30 minutes ago'
    },
    {
        icon: 'A',
        color: 'red',
        message: 'Your post in "Discussion Topic 3" was flagged for review.',
        time: '1 hour ago'
    }
];

const container = document.getElementById("notifications-container");

notifications.forEach(({ icon, color, message, time }) => {
    const div = document.createElement("div");
    div.className = `flex items-start sm:items-center gap-4 p-4 bg-gray-800 border border-gray-700 rounded-lg hover:bg-gray-700 transition-all`;

    div.innerHTML = `
      <div class="min-w-[44px] h-11 w-11 rounded-full bg-${color}-500/20 flex items-center justify-center">
        <span class="text-${color}-400 font-semibold text-sm">${icon}</span>
      </div>
      <div class="flex-1">
        <p class="text-sm font-medium text-gray-100 leading-snug">${message}</p>
        <p class="text-xs text-gray-400 mt-1">${time}</p>
      </div>
    `;

    container.appendChild(div);
});
