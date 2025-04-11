function renderUserList(users) {
    const leftPanel = document.getElementById("left-panel").querySelector(".space-y-4");
    leftPanel.innerHTML = "";

    users.forEach(user => {
        const img = user.img && user.img.trim() !== "" ? user.img : "../assets/profile.png";
        const lastMessage = user.last_message ? user.last_message : "click to chat";

        const userDiv = document.createElement("div");
        userDiv.className = "flex items-center justify-between gap-4 p-2 rounded hover:bg-gray-800 cursor-pointer";
        userDiv.id = user.user_id;
        userDiv.onclick = () => openChat(user.user_id, user.username, img);

        userDiv.innerHTML = `
            <div id="${user.user_id}" class="flex w-full items-center gap-4 overflow-hidden">
                <img src="${img}" class="w-10 h-10 rounded-full" />
                <div class="overflow-hidden w-full">
                    <div class="font-semibold sm:text-base text-sm">${user.username}</div>
                    <div class="text-sm w-full text-gray-400 truncate">${lastMessage}</div>
                </div>
            </div>
            <i class="fas fa-comment text-gray-500"></i>
        `;

        leftPanel.appendChild(userDiv);
    });
}

let currentChatUserId=null;

function openChat(userId, name, profile) {
    currentChatUserId = userId;
    document.getElementById("right-panel").classList.remove("hidden");
    document.getElementById("right-panel").classList.add("md:flex");
    document.querySelector("#right-panel img").src = profile;
    document.querySelector("#right-panel .font-semibold").innerText = name;

    const currentUserId = sessionStorage.getItem("userId");

    fetch("http://localhost:8000/chat/get", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            sender_id: currentUserId,
            receiver_id: userId
        })
    })
        .then(res => res.json())
        .then(data => {
            const chatContainer = document.querySelector("#right-panel .flex-1");
            chatContainer.innerHTML = "";

            data.data.forEach(msg => {
                const msgWrapper = document.createElement("div");
                msgWrapper.className = `flex flex-col ${msg.sender_id === currentUserId ? "items-end" : "items-start"}`;

                const msgDiv = document.createElement("div");
                msgDiv.className = `relative group px-4 py-2 rounded-2xl max-w-[80%] text-sm sm:text-base ${msg.sender_id === currentUserId ? "bg-blue-600 text-white" : "bg-gray-700 text-white"}`;
                msgDiv.textContent = msg.message;
                msgDiv.dataset.id = msg.message_id;

                if (msg.sender_id === currentUserId) {
                    msgDiv.addEventListener("dblclick", function (e) {
                        e.stopPropagation();
                        toggleActionButtons(msgDiv, msg);
                    });

                    let holdTimer = null;

                    const startHold = () => {
                        holdTimer = setTimeout(() => {
                            toggleActionButtons(msgDiv, msg);
                        }, 600);
                    };

                    const cancelHold = () => clearTimeout(holdTimer);

                    msgDiv.addEventListener("mousedown", startHold);
                    msgDiv.addEventListener("mouseup", cancelHold);
                    msgDiv.addEventListener("mouseleave", cancelHold);

                    msgDiv.addEventListener("touchstart", startHold);
                    msgDiv.addEventListener("touchend", cancelHold);
                    msgDiv.addEventListener("touchmove", cancelHold);
                    msgDiv.addEventListener("click", startHold);
                }

                const timeDiv = document.createElement("div");
                timeDiv.className = "text-xs text-gray-300 mt-1 pr-2";
                const time = new Date(msg.time).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: true
                });
                timeDiv.textContent = time;

                msgWrapper.appendChild(msgDiv);
                msgWrapper.appendChild(timeDiv);

                chatContainer.appendChild(msgWrapper);
            });

            chatContainer.scrollTop = chatContainer.scrollHeight;
        })
        .catch(err => {
            console.error("Error fetching chat messages:", err);
        });

    document.addEventListener("click", hideAllActionButtons);
}

function toggleActionButtons(msgDiv, msg) {
    const existing = msgDiv.querySelector(".chat-actions");
    if (existing) {
        existing.remove();
        return;
    }

    hideAllActionButtons();

    const actionContainer = document.createElement("div");
    actionContainer.className = `
        chat-actions absolute top-full right-2 mt-1 z-10 bg-gray-800 text-white text-sm rounded-lg shadow-lg
        flex-col py-1 px-2 space-y-1 w-32
    `;

    const actions = [
        {
            icon: "fas fa-pen",
            label: "Edit",
            class: "text-yellow-400",
            onClick: () => {
                const newText = prompt("Edit your message:", msg.message);
                if (newText && newText !== msg.message) {
                    editChatMessage(msg.message_id, newText);
                }
            }
        },
        {
            icon: "fas fa-trash",
            label: "Delete",
            class: "text-red-400",
            onClick: () => {
                if (confirm("Are you sure you want to delete this message?")) {
                    deleteChatMessage(msg.message_id);
                }
            }
        }
    ];

    actions.forEach(action => {
        const btn = document.createElement("button");
        btn.className = `flex items-center gap-2 w-full px-2 py-1 rounded hover:bg-gray-700 ${action.class}`;
        btn.innerHTML = `<i class="${action.icon}"></i> <span>${action.label}</span>`;
        btn.onclick = (e) => {
            e.stopPropagation();
            action.onClick();
            hideAllActionButtons();
        };
        actionContainer.appendChild(btn);
    });

    msgDiv.appendChild(actionContainer);
}

function hideAllActionButtons() {
    document.querySelectorAll(".chat-actions").forEach(el => el.remove());
}

function editChatMessage(messageId, newMessage) {
    const currentUserId = sessionStorage.getItem("userId");

    fetch("http://localhost:8000/chat/edit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: currentUserId,
            message_id: messageId,
            new_message: newMessage
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log("Message edited:", data);

            const oldMsgDiv = document.querySelector(`[data-id="${messageId}"]`);
            if (!oldMsgDiv) return;

            const newMsgDiv = document.createElement("div");
            newMsgDiv.className = "relative group px-4 py-2 rounded-2xl max-w-[80%] text-sm sm:text-base self-end bg-blue-600 text-white";
            newMsgDiv.textContent = newMessage;
            newMsgDiv.dataset.id = messageId;

            newMsgDiv.addEventListener("dblclick", function (e) {
                e.stopPropagation();
                toggleActionButtons(newMsgDiv, {
                    message_id: messageId,
                    message: newMessage
                });
            });

            let holdTimer = null;

            const startHold = () => {
                holdTimer = setTimeout(() => {
                    toggleActionButtons(newMsgDiv, {
                        message_id: messageId,
                        message: newMessage
                    });
                }, 600);
            };

            const cancelHold = () => clearTimeout(holdTimer);

            newMsgDiv.addEventListener("mousedown", startHold);
            newMsgDiv.addEventListener("mouseup", cancelHold);
            newMsgDiv.addEventListener("mouseleave", cancelHold);
            newMsgDiv.addEventListener("touchstart", startHold);
            newMsgDiv.addEventListener("touchend", cancelHold);
            newMsgDiv.addEventListener("touchmove", cancelHold);
            newMsgDiv.addEventListener("click", startHold);

            const parentWrapper = oldMsgDiv.parentElement;
            const timeDiv = parentWrapper.querySelector("div.text-xs");

            parentWrapper.innerHTML = "";
            parentWrapper.appendChild(newMsgDiv);
            if (timeDiv) parentWrapper.appendChild(timeDiv);
        })
        .catch(err => {
            console.error("Edit error:", err);
        });
    document.addEventListener("click", hideAllActionButtons);
}

function deleteChatMessage(messageId) {
    const currentUserId = sessionStorage.getItem("userId");

    fetch("http://localhost:8000/chat/delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: currentUserId,
            message_id: messageId
        })
    })
        .then(res => res.json())
        .then(data => {
            const msgDiv = document.querySelector(`[data-id="${messageId}"]`);
            if (msgDiv) {
                const wrapper = msgDiv.parentElement;
                wrapper.remove();
            }
        })
        .catch(err => {
            console.error("Delete error:", err);
        });
}

function closeChat() {
    document.getElementById("right-panel").classList.add("hidden");
}

const urlParams = new URLSearchParams(window.location.search);
const user_id = urlParams.get("userId");
const username = urlParams.get("username");
const img = urlParams.get("img");

if (user_id && username) {
    const userObject = {
        user_id: user_id,
        username: decodeURIComponent(username),
        img: decodeURIComponent(img || "../assets/profile.png"),
        last_message: "Click to chat"
    };
    renderUserList([userObject]);
} else {
    fetchPersonalChats();
}

const sendBtn = document.querySelector("#add-chat");
const messageInput = document.getElementById("message");

sendBtn.addEventListener("click", async () => {
    const messageText = messageInput.value.trim();
    if (!messageText) return;

    const now = new Date();
    const payload = {
        sender_id: sessionStorage.getItem("userId"),
        receiver_id: currentChatUserId,
        message: messageText,
        time: now.toISOString()
    };

    try {
        const res = await fetch("http://localhost:8000/chat/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Message failed");

        messageInput.value = "";

        const chatContainer = document.querySelector("#right-panel .flex-1");

        const msgWrapper = document.createElement("div");
        msgWrapper.className = "flex flex-col items-end";

        const msgDiv = document.createElement("div");
        msgDiv.className = "relative group px-4 py-2 rounded-2xl max-w-[80%] text-sm sm:text-base self-end bg-blue-600 text-white";
        msgDiv.textContent = data.data.message;
        msgDiv.dataset.id = data.data.message_id;

        msgDiv.addEventListener("dblclick", function (e) {
            e.stopPropagation();
            toggleActionButtons(msgDiv, {
                message_id: data.data.message_id,
                message: data.data.message
            });
        });

        let holdTimer = null;

        const startHold = () => {
            holdTimer = setTimeout(() => {
                toggleActionButtons(msgDiv, {
                    message_id: data.data.message_id,
                    message: data.data.message
                });
            }, 600);
        };

        const cancelHold = () => clearTimeout(holdTimer);

        msgDiv.addEventListener("mousedown", startHold);
        msgDiv.addEventListener("mouseup", cancelHold);
        msgDiv.addEventListener("mouseleave", cancelHold);
        msgDiv.addEventListener("touchstart", startHold);
        msgDiv.addEventListener("touchend", cancelHold);
        msgDiv.addEventListener("touchmove", cancelHold);
        msgDiv.addEventListener("click", startHold);

        const timeDiv = document.createElement("div");
        timeDiv.className = "text-xs text-gray-300 mt-1 pr-2";
        timeDiv.textContent = now.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
            hour12: true
        });

        msgWrapper.appendChild(msgDiv);
        msgWrapper.appendChild(timeDiv);
        chatContainer.appendChild(msgWrapper);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        console.log("Message sent:", data);
    } catch (err) {
        console.error("Error sending message:", err.message);
    }

    document.addEventListener("click", hideAllActionButtons);
});

async function fetchPersonalChats() {
    const userId = sessionStorage.getItem("userId");

    try {
        const res = await fetch(`http://localhost:8000/lastMessage/chats?user_id=${userId}`);
        const data = await res.json();

        if (!res.ok) throw new Error(data.detail || "Failed to fetch chats");
        if (data.data) {
            renderUserList(data.data);
        }
    } catch (err) {
        console.error("Error fetching chats:", err.message);
    }
}