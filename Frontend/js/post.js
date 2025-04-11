window.addEventListener("DOMContentLoaded", function () {
    const postData = JSON.parse(localStorage.getItem("selectedPost"));
    if (!postData) return;

    const container = document.getElementById("post-container");

    const timestamp = new Date(postData.timestamp);
    const date = timestamp.toLocaleDateString();
    const time = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const editedBadge = postData.edited === true
        ? `<div class="absolute bottom-36 right-4 bg-yellow-500 text-black text-xs sm:text-sm px-2 py-0.5 rounded">Edited</div>`
        : "";

    const html = `
        <div class="w-full relative">
    <img src="${postData.image_url}" onerror="this.onerror=null;this.src='../assets/post.png';" alt="Image" class="rounded-xl mb-3 sm:mb-4 w-full max-h-72 object-cover border-b">
    ${editedBadge}
    <h2 class="text-lg sm:text-xl font-bold mb-2 break-words px-6">${postData.title}</h2>
    <p class="text-gray-300 mb-4 text-sm sm:text-base leading-relaxed break-words px-6">
        ${postData.content}
    </p>
    <div class="flex flex-wrap justify-between items-center text-xs sm:text-sm text-gray-400 mb-4 px-6">
    <div class="flex justify-center items-center gap-4 profile-div" data-id="${postData.user_id}">
        <img class="w-12 h-12 rounded-full" src="${postData.img}" onerror="this.onerror=null;this.src='../assets/profile.png';" alt="profile">
        <div class="break-words">
            Posted by <span class="text-blue-400 font-medium">@${postData.username}</span><br>
            <span class="text-gray-500">${date}, ${time}</span>
        </div>
    </div>
        <div class="flex gap-3 mt-2 sm:mt-0">
            <span class="text-red-500 hover:text-red-600 text-base">
                <i class="fa-solid fa-flag"></i>
            </span>
        </div>
    </div>
    <div class="mb-4 px-6">
    <div class="text-xs font-semibold text-gray-400 mb-1">Tags:</div>
    <div class="flex flex-wrap gap-2 text-xs break-words">
    ${postData.tags?.split(',').map(tag => `<span class="bg-gray-700 px-3 py-1 rounded-full text-green-300">#${tag.trim()}</span>`).join('') || ''}
    </div>
    </div>
    <div class="mb-3 px-6">
        <div class="text-xs font-semibold text-gray-400 mb-1">Category:</div>
        <div class="bg-gray-700 inline-block px-3 py-1 rounded-full text-blue-300 text-xs break-words">${postData.category_name}</div>
    </div>
    <div class="border-t border-gray-700 py-4 text-sm text-gray-300 px-6 cursor-pointer">
        <div class="flex justify-around mb-2">
            <div class="flex flex-col items-center">
                <span class="text-green-400 hover:text-green-300 text-base">
                    <i id="upvote-icon" class="fa-regular fa-thumbs-up"></i>
                </span>
                <span id="upvote-count">${postData.upvotes}</span>
            </div>
            <div class="flex flex-col items-center">
                <span class="text-red-400 hover:text-red-300 text-base">
                    <i id="downvote-icon" class="fa-regular fa-thumbs-down"></i>
                </span>
                <span id="downvote-count">${postData.downvotes}</span>
            </div>
            <div class="flex flex-col items-center">
                <span class="text-cyan-600 text-sm sm:text-base">
                    <i class="fa-regular fa-eye"></i>
                </span>
                <span id="view-count">${postData.views}</span>
            </div>
            <div class="flex flex-col items-center">
                <span class="text-purple-800 text-sm sm:text-base">
                    <i class="fa-regular fa-comment-dots"></i>
                </span>
                <span id="comment-count">${postData.comment_count}</span>
            </div>
        </div>
        <div class="flex justify-around">
            <div class="flex flex-col items-center">
                <span class="text-yellow-400 hover:text-yellow-300 text-sm sm:text-base">
                    <i class="fa-solid fa-share-nodes"></i>
                </span>
                <span id="share-count">${postData.shared}</span>
            </div>
            <div class="flex flex-col items-center">
                <span class="text-purple-400 hover:text-purple-300 text-sm sm:text-base">
                    <i id="bookmark-icon" class="fa-regular fa-bookmark"></i>
                </span>
                <span id="bookmark-count">${postData.bookmark_count}</span>
            </div>
            <div class="flex flex-col items-center">
                <span class="text-emerald-400 hover:text-blue-300 text-sm sm:text-base">
                    <i id="followed-icon" class="fa-regular fa-square-plus"></i>
                </span>
                <span id="followed-count">${postData.followed}</span>
            </div>
            <div class="flex flex-col items-center">
                <span class="text-blue-400 hover:text-blue-300 text-sm sm:text-base">
                    <i id="following-icon" class="fa-regular fa-user"></i>
                </span>
                <span id="followers-count">0</span>
            </div>
        </div>
    </div>
</div>
    `;

    container.innerHTML = html;
    countView(postData.post_id);
    getVote(postData.post_id);
    getBookmark(postData.post_id);
    getFollowThread(postData.post_id);
    updateFormattedCounts();
    document.getElementById("upvote-count").parentElement.addEventListener("click", function () {
        addVote(postData.post_id, "upvote");
    });

    document.getElementById("downvote-count").parentElement.addEventListener("click", function () {
        addVote(postData.post_id, "downvote");
    });

    document.getElementById("comment-count").parentElement.addEventListener("click", function () {
        getComment(postData.post_id);
    });

    document.getElementById("share-count").parentElement.addEventListener("click", function () {
        handleShare(postData.post_id);
    });

    document.getElementById("bookmark-count").parentElement.addEventListener("click", function () {
        addBookmark(postData.post_id, true);
    });

    document.getElementById("followed-count").parentElement.addEventListener("click", function () {
        addToFollowThread(postData.post_id, true);
    });
    if (postData.is_locked === "True") {
        const commentInput = document.getElementById("comment-input");
        if (commentInput) {
            commentInput.remove();
        }
        const commentContainer = document.getElementById("comment-container");
        if (commentContainer) {
            commentContainer.innerHTML = `
            <div class="text-center text-sm sm:text-base text-red-400 py-4">
                    Comments are locked for this post.
                    </div>
                    `;
        }
    } else {
        getComments(postData.post_id);
    }
});

async function addVote(postId, voteType) {
    try {
        const response = await fetch("http://localhost:8000/vote/addVote", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                post_id: postId,
                user_id: sessionStorage.getItem("userId"),
                vote_type: voteType,
            }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to add vote");
        }
        const responseData = await response.json();
        if (responseData.message === "Upvote added.") {
            let count = document.getElementById("upvote-count").innerText;
            count = parseInt(count) + 1;
            document.getElementById("upvote-count").innerText = formatCount(count);
            document.getElementById("upvote-count").innerText = formatCount(count);
            document.getElementById("upvote-icon").classList.remove("fa-regular");
            document.getElementById("upvote-icon").classList.add("fa-solid");
            document.getElementById("downvote-icon").classList.remove("fa-solid");
            document.getElementById("downvote-icon").classList.add("fa-regular");
        }
        if (responseData.message === "Downvote added.") {
            let count = document.getElementById("downvote-count").innerText;
            count = parseInt(count) + 1;
            document.getElementById("downvote-count").innerText = formatCount(count);
            document.getElementById("downvote-icon").classList.remove("fa-regular");
            document.getElementById("downvote-icon").classList.add("fa-solid");
            document.getElementById("upvote-icon").classList.remove("fa-solid");
            document.getElementById("upvote-icon").classList.add("fa-regular");
        }
        if (responseData.message === "Upvote removed.") {
            let count = document.getElementById("upvote-count").innerText;
            count = parseInt(count) - 1;
            document.getElementById("upvote-count").innerText = formatCount(count);
            document.getElementById("upvote-icon").classList.remove("fa-solid");
            document.getElementById("upvote-icon").classList.add("fa-regular");
        }
        if (responseData.message === "Downvote removed.") {
            let count = document.getElementById("downvote-count").innerText;
            count = parseInt(count) - 1;
            document.getElementById("downvote-count").innerText = formatCount(count);
            document.getElementById("downvote-icon").classList.remove("fa-solid");
            document.getElementById("downvote-icon").classList.add("fa-regular");
        }
        if (responseData.message === "Vote updated from Upvote to Downvote.") {
            let countVote = document.getElementById("upvote-count").innerText;
            countVote = parseInt(countVote) - 1;
            document.getElementById("upvote-count").innerText = formatCount(countVote);
            let countDownvote = document.getElementById("downvote-count").innerText;
            countDownvote = parseInt(countDownvote) + 1;
            document.getElementById("downvote-count").innerText = formatCount(countDownvote);
            document.getElementById("downvote-icon").classList.remove("fa-regular");
            document.getElementById("downvote-icon").classList.add("fa-solid");
            document.getElementById("upvote-icon").classList.remove("fa-solid");
            document.getElementById("upvote-icon").classList.add("fa-regular");
        }
        if (responseData.message === "Vote updated from Downvote to Upvote.") {
            let countDownvote = document.getElementById("downvote-count").innerText;
            countDownvote = parseInt(countDownvote) - 1;
            document.getElementById("downvote-count").innerText = formatCount(countDownvote);
            let countVote = document.getElementById("upvote-count").innerText;
            countVote = parseInt(countVote) + 1;
            document.getElementById("upvote-count").innerText = formatCount(countVote);
            document.getElementById("upvote-icon").classList.remove("fa-regular");
            document.getElementById("upvote-icon").classList.add("fa-solid");
            document.getElementById("downvote-icon").classList.remove("fa-solid");
            document.getElementById("downvote-icon").classList.add("fa-regular");
        }
    } catch (error) {
        console.error("Error adding vote:", error);
        throw error;
    }
}

async function getVote(postId) {
    try {
        const response = await fetch("http://localhost:8000/vote/getVote", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                post_id: postId,
                user_id: sessionStorage.getItem("userId"),
            }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to get vote");
        }
        const responseData = await response.json();
        if (responseData.data.vote_type === "upvote") {
            document.getElementById("upvote-icon").classList.remove("fa-regular");
            document.getElementById("upvote-icon").classList.add("fa-solid");
            document.getElementById("downvote-icon").classList.remove("fa-solid");
            document.getElementById("downvote-icon").classList.add("fa-regular");
        } else if (responseData.data.vote_type === "downvote") {
            document.getElementById("downvote-icon").classList.remove("fa-regular");
            document.getElementById("downvote-icon").classList.add("fa-solid");
            document.getElementById("upvote-icon").classList.remove("fa-solid");
            document.getElementById("upvote-icon").classList.add("fa-regular");
        }
        if (responseData.data) {
            document.getElementById("upvote-count").innerText = formatCount(responseData.data.upvotes);
            document.getElementById("downvote-count").innerText = formatCount(responseData.data.downvotes);
        }
    } catch (error) {
        console.error("Error getting vote:", error);
        return null;
    }
}

async function countView(postId) {
    try {
        const response = await fetch("http://localhost:8000/post/countView", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                post_id: postId,
                user_id: sessionStorage.getItem("userId"),
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to count view");
        }

        const responseData = await response.json();
        if (responseData.message) {
            document.getElementById("view-count").innerText = formatCount(responseData.data[0]);
        }
    } catch (error) {
        console.error("Error counting view:", error);
        return null;
    }
}

function updateFormattedCounts() {
    const countIds = [
        'upvote-count',
        'downvote-count',
        'view-count',
        'comment-count',
        'share-count',
        'bookmark-count',
        'followed-count',
        'followers-count'
    ];

    countIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            const value = parseInt(el.innerText);
            if (!isNaN(value)) {
                el.innerText = formatCount(value);
            }
        }
    });
}

function formatCount(num) {
    if (num >= 1_000_000) {
        return (num / 1_000_000).toFixed(1).replace(/\.0$/, '') + 'M';
    } else if (num >= 1_000) {
        return (num / 1_000).toFixed(1).replace(/\.0$/, '') + 'k';
    } else {
        return num.toString();
    }
}

async function addBookmark(postId, type) {
    try {
        const response = await fetch("http://localhost:8000/bookmark/addBookmark", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                post_id: postId,
                user_id: sessionStorage.getItem("userId"),
                type: type,
            }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to add vote");
        }
        const responseData = await response.json();
        if (responseData.message === "Bookmark removed.") {
            let count = document.getElementById("bookmark-count").innerText;
            count = parseInt(count) - 1;
            document.getElementById("bookmark-count").innerText = formatCount(count);
            document.getElementById("bookmark-icon").classList.remove("fa-solid");
            document.getElementById("bookmark-icon").classList.add("fa-regular");
        }
        if (responseData.message === "Bookmark added.") {
            let count = document.getElementById("bookmark-count").innerText;
            count = parseInt(count) + 1;
            document.getElementById("bookmark-count").innerText = formatCount(count);
            document.getElementById("bookmark-icon").classList.remove("fa-regular");
            document.getElementById("bookmark-icon").classList.add("fa-solid");
        }
    } catch (error) {
        console.error("Error adding vote:", error);
        throw error;
    }
}

async function getBookmark(postId) {
    try {
        const response = await fetch("http://localhost:8000/bookmark/getBookmark", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                post_id: postId,
                user_id: sessionStorage.getItem("userId"),
            }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to get vote");
        }
        const responseData = await response.json();
        if (responseData.message) {
            document.getElementById("bookmark-count").innerText = formatCount(responseData.data.bookmark_count);
            if (responseData.data.is_bookmarked === true) {
                document.getElementById("bookmark-icon").classList.remove("fa-regular");
                document.getElementById("bookmark-icon").classList.add("fa-solid");
            } else {
                document.getElementById("bookmark-icon").classList.remove("fa-solid");
                document.getElementById("bookmark-icon").classList.add("fa-regular");
            }
        }
    } catch (error) {
        console.error("Error getting vote:", error);
        return null;
    }
}

async function addToFollowThread(postId, type) {
    try {
        const response = await fetch("http://localhost:8000/thread/followThread", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                post_id: postId,
                user_id: sessionStorage.getItem("userId"),
                type: type,
            }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to add vote");
        }
        const responseData = await response.json();
        if (responseData.message === "Thread unfollowed.") {
            let count = document.getElementById("followed-count").innerText;
            count = parseInt(count) - 1;
            document.getElementById("followed-count").innerText = formatCount(count);
            document.getElementById("followed-icon").classList.remove("fa-solid");
            document.getElementById("followed-icon").classList.add("fa-regular");
        }
        if (responseData.message === "Thread followed.") {
            let count = document.getElementById("followed-count").innerText;
            count = parseInt(count) + 1;
            document.getElementById("followed-count").innerText = formatCount(count);
            document.getElementById("followed-icon").classList.remove("fa-regular");
            document.getElementById("followed-icon").classList.add("fa-solid");
        }
    } catch (error) {
        console.error("Error adding vote:", error);
        throw error;
    }
}

async function getFollowThread(postId) {
    try {
        const response = await fetch("http://localhost:8000/thread/getFollowThread", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                post_id: postId,
                user_id: sessionStorage.getItem("userId"),
            }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to get vote");
        }
        const responseData = await response.json();
        if (responseData.message) {
            document.getElementById("followed-count").innerText = formatCount(responseData.data.follow_count);
            if (responseData.data.is_following === true) {
                document.getElementById("followed-icon").classList.remove("fa-regular");
                document.getElementById("followed-icon").classList.add("fa-solid");
            } else {
                document.getElementById("followed-icon").classList.remove("fa-solid");
                document.getElementById("followed-icon").classList.add("fa-regular");
            }
        }
    } catch (error) {
        console.error("Error getting vote:", error);
        return null;
    }
}

const container = document.getElementById("comment-container");
container.innerHTML = "";
let allComments = [];

function renderComments(comments) {
    const container = document.getElementById("comment-container");
    const currentUserId = sessionStorage.getItem("userId");

    comments.forEach(comment => {
        allComments.push(comment);
        const div = document.createElement("div");
        div.className = "bg-gray-900 rounded-lg p-3 relative";
        div.setAttribute("data-id", comment.comment_id);

        const isOwner = currentUserId === comment.user_id;
        const displayName = isOwner ? "You" : comment.username;

        let isEdited = false;
        let rawTime = comment.time;
        if (rawTime.endsWith(" (edited)")) {
            isEdited = true;
            rawTime = rawTime.replace(" (edited)", "");
        }
        const timeAgo = formatTimeAgo(rawTime) + (isEdited ? " (edited)" : "");

        let optionsMenu = '';
        if (isOwner) {
            optionsMenu = `
                <button class="edit-btn flex items-center gap-2 px-3 py-2 hover:bg-gray-700 w-full text-left" data-id="${comment.comment_id}">
                    <i class="text-blue-400 fas fa-pen text-xs"></i> Edit
                </button>
                <button class="delete-btn flex items-center gap-2 px-3 py-2 hover:bg-gray-700 w-full text-left" data-id="${comment.comment_id}">
                    <i class="text-red-400 fas fa-trash text-xs"></i> Delete
                </button>
            `;
        } else {
            optionsMenu = `
                <button class="flex items-center gap-2 px-3 py-2 hover:bg-gray-700 w-full text-left">
                    <i class="text-red-400 fas fa-flag text-xs"></i> Report
                </button>
            `;
        }

        div.innerHTML = `
            <div class="flex justify-between">
                <div class="flex">
                    <img src="${comment.img}" onerror="this.onerror=null;this.src='../assets/profile.png';" alt="profile" class="w-10 h-10 rounded-full mr-3">
                    <div>
                        <p class="text-white font-semibold text-sm">${displayName}</p>
                        <p class="comment-time text-gray-400 text-xs">${timeAgo}</p>
                    </div>
                </div>
                <div class="relative">
                    <button class="text-gray-300 hover:text-white options-btn text-xl" data-id="${comment.comment_id}">⋮</button>
                    <div class="absolute top-6 right-0 bg-gray-800 text-white rounded shadow hidden options-menu z-10 w-32 text-sm">
                        ${optionsMenu}
                    </div>
                </div>
            </div>
            <div class="comment-content mt-2 text-gray-200 text-sm">${comment.content}</div>
            <div class="mt-3 flex items-center space-x-4 text-gray-400 text-sm">
                <button><i class="text-green-400 fa-regular fa-thumbs-up upvote" data-id="${comment.comment_id}"></i><span class="ml-1 upvote-count">${comment.upvotes || 0}</span></button>
                <button><i class="text-red-400 fa-regular fa-thumbs-down downvote" data-id="${comment.comment_id}"></i><span class="ml-1 downvote-count">${comment.upvotes || 0}</span></button>
                <button class="reply-toggle" data-id="${comment.comment_id}">
                    <i class="text-blue-400 fas fa-reply"></i> Reply (${comment.reply_count || 0})
                </button>
            </div>
            <div class="reply-container hidden mt-4 pl-4 border-l border-gray-600 space-y-4" id="reply-container-${comment.comment_id}">
            </div>
        `;
        getCommentVote(comment.comment_id);
        getReplies(comment.comment_id);
        container.appendChild(div);
    });
}

function formatTimeAgo(isoTime) {
    const time = new Date(isoTime);
    const now = new Date();
    const seconds = Math.floor((now - time) / 1000);

    if (seconds < 60) return `${seconds} second${seconds !== 1 ? 's' : ''} ago`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    const days = Math.floor(hours / 24);
    if (days === 1) return "Yesterday";
    if (days < 30) return `${days} day${days !== 1 ? 's' : ''} ago`;
    const months = Math.floor(days / 30);
    if (months < 12) return `${months} month${months !== 1 ? 's' : ''} ago`;
    const years = Math.floor(months / 12);
    return `${years} year${years !== 1 ? 's' : ''} ago`;
}

document.addEventListener("click", function (e) {
    if (e.target.closest(".options-btn")) {
        const btn = e.target.closest(".options-btn");
        const menu = btn.nextElementSibling;
        const isHidden = menu.classList.contains("hidden");

        document.querySelectorAll(".options-menu").forEach(m => m.classList.add("hidden"));

        if (isHidden) {
            menu.classList.remove("hidden");
        } else {
            menu.classList.add("hidden");
        }
        return;
    }

    if (e.target.closest(".edit-btn")) {
        const commentId = e.target.closest(".edit-btn").dataset.id;
        handleEditComment(commentId);
        document.querySelectorAll(".options-menu").forEach(menu => menu.classList.add("hidden"));
        return;
    }

    if (e.target.closest(".edit-reply-btn")) {
        const replyId = e.target.closest(".edit-reply-btn").id;
        const commentId = e.target.closest(".edit-reply-btn").dataset.id;
        handleEditReply(replyId, commentId);
        document.querySelectorAll(".options-menu").forEach(menu => menu.classList.add("hidden"));
        return;
    }

    if (e.target.closest(".upvote")) {
        const commentId = e.target.closest(".upvote").dataset.id;
        addVoteToComment(commentId, "upvote");
        return;
    }

    if (e.target.closest(".downvote")) {
        const commentId = e.target.closest(".downvote").dataset.id;
        addVoteToComment(commentId, "downvote");
        return;
    }

    if (e.target.closest(".upvote-reply")) {
        const replyId = e.target.closest(".upvote-reply").dataset.id;
        addVoteToReply(replyId, "upvote");
        return;
    }

    if (e.target.closest(".downvote-reply")) {
        const replyId = e.target.closest(".downvote-reply").dataset.id;
        addVoteToReply(replyId, "downvote");
        return;
    }

    if (e.target.closest(".delete-btn")) {
        const commentId = e.target.closest(".delete-btn").dataset.id;
        const confirmDelete = confirm("Are you sure you want to delete this comment?");
        if (confirmDelete) {
            deleteComment(commentId);
        }
        document.querySelectorAll(".options-menu").forEach(menu => menu.classList.add("hidden"));
        return;
    }

    if (e.target.closest(".delete-reply-btn")) {
        const commentId = e.target.closest(".delete-reply-btn").dataset.id;
        const replyId = e.target.closest(".delete-reply-btn").id;
        const confirmDelete = confirm("Are you sure you want to delete this reply?");
        if (confirmDelete) {
            deleteReply(commentId, replyId);
        }
        document.querySelectorAll(".options-menu").forEach(menu => menu.classList.add("hidden"));
        return;
    }

    document.querySelectorAll(".options-menu").forEach(menu => menu.classList.add("hidden"));

    if (e.target.closest(".reply-toggle")) {
        const id = e.target.closest(".reply-toggle").dataset.id;
        const replyContainer = document.getElementById(`reply-container-${id}`);
        replyContainer.classList.toggle("hidden");
        addReplyInput(replyContainer, id);
    }

    if (e.target.closest(".profile-div")) {
        const id = e.target.closest(".profile-div").dataset.id;
        window.location.href = "./profile.html?id=" + id;
    }
});

function addReplyInput(container, commentId) {
    if (container.querySelector(".reply-box")) return;
    const replyBox = document.createElement("div");
    replyBox.className = "reply-box mt-3 flex items-start gap-2";
    replyBox.innerHTML = `
        <textarea id="new-reply" class="reply-text flex-1 p-2 rounded bg-gray-800 text-white text-sm" rows="1" placeholder="Write a reply..."></textarea>
        <button class="add-reply-btn text-blue-400 hover:text-blue-600 mt-1">
            <i class="fas fa-paper-plane text-lg"></i>
        </button>
    `;

    container.appendChild(replyBox);

    const replyTextarea = replyBox.querySelector(".reply-text");
    const addReplyBtn = replyBox.querySelector(".add-reply-btn");

    addReplyBtn.addEventListener("click", function () {
        const reply = replyTextarea.value;
        postReply(commentId, reply);
        replyTextarea.value = "";
    });
}

document.getElementById("postComment").addEventListener("click", postComment);

async function postComment() {
    const textarea = document.getElementById("new-comment");
    const comment = textarea.value.trim();

    if (!comment) {
        alert("Comment can't be empty.");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/comment/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: comment, user_id: sessionStorage.getItem("userId"), post_id: JSON.parse(localStorage.getItem("selectedPost")).post_id })
        });

        const result = await response.json();

        if (result) {
            renderComments([result.data]);
            let count = document.getElementById("comment-count").innerText;
            count = parseInt(count) + 1;
            document.getElementById("comment-count").innerText = formatCount(count);
            textarea.value = "";
        } else {
            console.error("Failed to post comment:", result.message);
            alert("Failed to post comment.");
        }
    } catch (error) {
        console.error("Error posting comment:", error);
        alert("Something went wrong. Please try again.");
    }
}

async function getComments(postId) {
    try {
        const response = await fetch("http://localhost:8000/comment/get", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ post_id: postId })
        });

        const result = await response.json();

        if (result) {
            let totalComments = result.data.length;
            document.getElementById("comment-count").innerText = formatCount(totalComments);
            renderComments(result.data);
        } else {
            console.error("Failed to post comment:", result.message);
            alert("Failed to post comment.");
        }
    } catch (error) {
        console.error("Error posting comment:", error);
        alert("Something went wrong. Please try again.");
    }
}

async function deleteComment(comment_id) {
    let post_id = JSON.parse(localStorage.getItem("selectedPost")).post_id;
    try {
        const response = await fetch('http://127.0.0.1:8000/comment/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ post_id, comment_id })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to delete comment');
        }
        if (data.data) {
            document.querySelector(`[data-id='${data.data.comment_id}']`).remove();
            let count = document.getElementById("comment-count").innerText;
            count = parseInt(count) - 1;
            document.getElementById("comment-count").innerText = formatCount(count);
        }
    } catch (error) {
        console.error('Error deleting comment:', error.message);
    }
}

let originalCommentText = "";

function handleEditComment(commentId) {
    const commentDiv = document.querySelector(`[data-id="${commentId}"]`);
    if (!commentDiv) {
        console.error("Comment div not found for id:", commentId);
        return;
    }

    const contentEl = commentDiv.querySelector(".comment-content");
    const originalContent = contentEl.textContent;

    contentEl.setAttribute("data-original", originalContent);

    contentEl.innerHTML = `
        <textarea id="edit-comment" class="edit-input bg-gray-800 text-white px-2 py-1 rounded w-full resize-none" rows="3">${originalContent}</textarea>
        <div class="mt-2 space-x-2 text-lg text-right">
            <i class="confirm-edit fa-solid fa-check cursor-pointer text-green-500 hover:text-green-300"></i>
            <i class="cancel-edit fa-solid fa-times cursor-pointer text-red-500 hover:text-red-300"></i>
        </div>
    `;

    const input = contentEl.querySelector(".edit-input");
    const confirmBtn = contentEl.querySelector(".confirm-edit");
    const cancelBtn = contentEl.querySelector(".cancel-edit");

    confirmBtn.addEventListener("click", () => {
        const newContent = input.value.trim();
        if (!newContent) {
            alert("Comment cannot be empty.");
            return;
        }

        if (newContent === originalContent) {
            alert("No changes made to the comment.");
            return;
        }

        confirmBtn.classList.add("opacity-50", "pointer-events-none");

        contentEl.innerHTML = newContent;
        editComment(commentId, newContent);
    });

    cancelBtn.addEventListener("click", () => {
        contentEl.textContent = contentEl.getAttribute("data-original");
    });
}

function editComment(commentId, newContent) {
    fetch("http://127.0.0.1:8000/comment/edit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            comment_id: commentId,
            user_id: sessionStorage.getItem("userId"),
            post_id: JSON.parse(localStorage.getItem("selectedPost")).post_id,
            new_content: newContent
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                const commentDiv = document.querySelector(`[data-id="${commentId}"]`);
                const contentEl = commentDiv.querySelector(".comment-content");
                const timeEl = commentDiv.querySelector(".comment-time");

                contentEl.innerHTML = data.data.content;

                if (timeEl) {
                    let isEdited = false;
                    let rawTime = data.data.time;
                    if (rawTime.endsWith(" (edited)")) {
                        isEdited = true;
                        rawTime = rawTime.replace(" (edited)", "");
                    }
                    const timeAgo = formatTimeAgo(rawTime) + (isEdited ? " (edited)" : "");
                    timeEl.innerText = timeAgo;
                }
            } else {
                alert(data.message || "Failed to edit comment.");
            }
        })
        .catch(err => {
            console.error("Edit error:", err);
            alert("Something went wrong.");
        });
}

async function addVoteToComment(commentID, voteType) {
    try {
        const response = await fetch("http://localhost:8000/voteComment/addCommentVote", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                comment_id: commentID,
                user_id: sessionStorage.getItem("userId"),
                vote_type: voteType,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to add vote");
        }

        const responseData = await response.json();

        const upvoteIcon = document.querySelector(`.upvote[data-id='${commentID}']`);
        const downvoteIcon = document.querySelector(`.downvote[data-id='${commentID}']`);

        const upvoteCountEl = upvoteIcon.closest("button").querySelector(".upvote-count");
        const downvoteCountEl = downvoteIcon.closest("button").querySelector(".downvote-count");

        let upvoteCount = parseInt(upvoteCountEl?.textContent.trim() || 0);
        let downvoteCount = parseInt(downvoteCountEl?.textContent.trim() || 0);

        switch (responseData.message) {
            case "Upvote added.":
                upvoteCount++;
                upvoteIcon.classList.replace("fa-regular", "fa-solid");
                downvoteIcon.classList.replace("fa-solid", "fa-regular");
                break;
            case "Downvote added.":
                downvoteCount++;
                downvoteIcon.classList.replace("fa-regular", "fa-solid");
                upvoteIcon.classList.replace("fa-solid", "fa-regular");
                break;
            case "Upvote removed.":
                upvoteCount--;
                upvoteIcon.classList.replace("fa-solid", "fa-regular");
                break;
            case "Downvote removed.":
                downvoteCount--;
                downvoteIcon.classList.replace("fa-solid", "fa-regular");
                break;
            case "Vote updated from upvote to downvote.":
                upvoteCount--;
                downvoteCount++;
                upvoteIcon.classList.replace("fa-solid", "fa-regular");
                downvoteIcon.classList.replace("fa-regular", "fa-solid");
                break;
            case "Vote updated from downvote to upvote.":
                downvoteCount--;
                upvoteCount++;
                downvoteIcon.classList.replace("fa-solid", "fa-regular");
                upvoteIcon.classList.replace("fa-regular", "fa-solid");
                break;
        }

        if (upvoteCountEl) upvoteCountEl.textContent = `${formatCount(upvoteCount)}`;
        if (downvoteCountEl) downvoteCountEl.textContent = `${formatCount(downvoteCount)}`;

    } catch (error) {
        console.error("Error adding vote:", error);
    }
}

async function getCommentVote(commentId) {
    try {
        const response = await fetch("http://localhost:8000/voteComment/getCommentVote", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                comment_id: commentId,
                user_id: sessionStorage.getItem("userId"),
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to get vote");
        }

        const responseData = await response.json();

        const upvoteIcon = document.querySelector(`.upvote[data-id='${commentId}']`);
        const downvoteIcon = document.querySelector(`.downvote[data-id='${commentId}']`);
        const upvoteCountEl = upvoteIcon.nextSibling;
        const downvoteCountEl = downvoteIcon.nextSibling;

        if (responseData.data.vote_type === "upvote") {
            upvoteIcon.classList.replace("fa-regular", "fa-solid");
            downvoteIcon.classList.replace("fa-solid", "fa-regular");
        } else if (responseData.data.vote_type === "downvote") {
            downvoteIcon.classList.replace("fa-regular", "fa-solid");
            upvoteIcon.classList.replace("fa-solid", "fa-regular");
        }

        if (responseData.data) {
            upvoteCountEl.textContent = ` ${formatCount(responseData.data.upvotes)}`;
            downvoteCountEl.textContent = ` ${formatCount(responseData.data.downvotes)}`;
        }

    } catch (error) {
        console.error("Error getting vote:", error);
    }
}

let allreplies = [];

function renderReplies(replies, commentId) {
    const container = document.getElementById(`reply-container-${commentId}`);
    const currentUserId = sessionStorage.getItem("userId");

    replies.forEach(reply => {
        allreplies.push(reply);
        const div = document.createElement("div");
        div.className = "bg-gray-900 rounded-lg p-3 relative";
        div.setAttribute("data-id", reply.reply_id);

        const isOwner = currentUserId === reply.user_id;
        const displayName = isOwner ? "You" : reply.username;

        let isEdited = false;
        let rawTime = reply.time;
        if (rawTime.endsWith(" (edited)")) {
            isEdited = true;
            rawTime = rawTime.replace(" (edited)", "");
        }
        const timeAgo = formatTimeAgo(rawTime) + (isEdited ? " (edited)" : "");

        let optionsMenu = '';
        if (isOwner) {
            optionsMenu = `
                <button class="edit-reply-btn flex items-center gap-2 px-3 py-2 hover:bg-gray-700 w-full text-left" id="${reply.reply_id}" data-id="${commentId}">
                    <i class="text-blue-400 fas fa-pen text-xs"></i> Edit
                </button>
                <button class="delete-reply-btn flex items-center gap-2 px-3 py-2 hover:bg-gray-700 w-full text-left" id="${reply.reply_id}" data-id="${commentId}">
                    <i class="text-red-400 fas fa-trash text-xs"></i> Delete
                </button>
            `;
        } else {
            optionsMenu = `
                <button class="flex items-center gap-2 px-3 py-2 hover:bg-gray-700 w-full text-left">
                    <i class="text-red-400 fas fa-flag text-xs"></i> Report
                </button>
            `;
        }

        div.innerHTML = `
            <div class="flex justify-between">
                <div class="flex">
                    <img src="${reply.img}" onerror="this.onerror=null;this.src='../assets/profile.png';" alt="profile" class="w-10 h-10 rounded-full mr-3">
                    <div>
                        <p class="text-white font-semibold text-sm">${displayName}</p>
                        <p class="reply-time text-gray-400 text-xs">${timeAgo}</p>
                    </div>
                </div>
                <div class="relative">
                    <button class="text-gray-300 hover:text-white options-btn text-xl" data-id="${reply.reply_id}">⋮</button>
                    <div class="absolute top-6 right-0 bg-gray-800 text-white rounded shadow hidden options-menu z-10 w-32 text-sm">
                        ${optionsMenu}
                    </div>
                </div>
            </div>
            <div class="reply-content mt-2 text-gray-200 text-sm">${reply.content}</div>
            <div class="mt-3 flex items-center space-x-4 text-gray-400 text-sm">
                <button><i class="text-green-400 fa-regular fa-thumbs-up upvote-reply" data-id="${reply.reply_id}"></i><span class="ml-1 upvote-reply-count">${reply.upvotes || 0}</span></button>
                <button><i class="text-red-400 fa-regular fa-thumbs-down downvote-reply" data-id="${reply.reply_id}"></i><span class="ml-1 downvote-reply-count">${reply.downvote || 0}</span></button>
            </div>
            <div class="reply-container hidden mt-4 pl-4 border-l border-gray-600 space-y-4" id="reply-container-${reply.reply_id}">
            </div>
        `;
        getReplyVote(reply.reply_id);
        container.prepend(div);
    });
}

async function postReply(commentId, value) {
    const reply = value.trim();

    if (!reply) {
        alert("Reply can't be empty.");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/reply/addReply", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: reply, user_id: sessionStorage.getItem("userId"), comment_id: commentId })
        });

        const result = await response.json();

        if (result) {
            renderReplies([result.data], result.data.comment_id);
        } else {
            console.error("Failed to post comment:", result.message);
            alert("Failed to post comment.");
        }
    } catch (error) {
        console.error("Error posting comment:", error);
        alert("Something went wrong. Please try again.");
    }
}

async function getReplies(commentId) {
    try {
        const response = await fetch("http://localhost:8000/reply/getReplies", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ comment_id: commentId })
        });

        const result = await response.json();

        if (result && Array.isArray(result.data) && result.data.length > 0) {
            let length = result.data.length;
            const button = document.querySelector(`.reply-toggle[data-id="${commentId}"]`);
            button.innerHTML = `<i class="text-blue-400 fas fa-reply"></i> Reply (${length})`;
            renderReplies(result.data, commentId);
        }
        if (result.detail) {
            console.error("Failed to post comment:", result.detail);
            alert("Failed to post comment.");
        }
    } catch (error) {
        console.error("Error posting comment:", error);
        alert("Something went wrong. Please try again.");
    }
}

function handleEditReply(commentId, replyId) {
    const replyDiv = document.querySelector(`[data-id="${replyId}"]`);
    if (!replyDiv) {
        console.error("Comment div not found for id:", replyId);
        return;
    }

    const contentEl = replyDiv.querySelector(".reply-content");
    const originalContent = contentEl.textContent;

    contentEl.setAttribute("data-original", originalContent);

    contentEl.innerHTML = `
        <textarea id="edit-reply" class="edit-input bg-gray-800 text-white px-2 py-1 rounded w-full resize-none" rows="3">${originalContent}</textarea>
        <div class="mt-2 space-x-2 text-lg text-right">
            <i class="confirm-edit fa-solid fa-check cursor-pointer text-green-500 hover:text-green-300"></i>
            <i class="cancel-edit fa-solid fa-times cursor-pointer text-red-500 hover:text-red-300"></i>
        </div>
    `;

    const input = contentEl.querySelector(".edit-input");
    const confirmBtn = contentEl.querySelector(".confirm-edit");
    const cancelBtn = contentEl.querySelector(".cancel-edit");

    confirmBtn.addEventListener("click", () => {
        const newContent = input.value.trim();
        if (!newContent) {
            alert("Reply cannot be empty.");
            return;
        }
        if (newContent === originalContent) {
            alert("No changes made to the reply.");
            return;
        }
        confirmBtn.classList.add("opacity-50", "pointer-events-none");

        contentEl.innerHTML = newContent;
        editReply(replyId, newContent, commentId);
    });

    cancelBtn.addEventListener("click", () => {
        contentEl.textContent = contentEl.getAttribute("data-original");
    });
}

function editReply(commentId, newContent, replyId) {
    fetch("http://127.0.0.1:8000/reply/editReply", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            reply_id: replyId,
            user_id: sessionStorage.getItem("userId"),
            comment_id: commentId,
            new_content: newContent
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                const commentDiv = document.querySelector(`[data-id="${replyId}"]`);
                const contentEl = commentDiv.querySelector(".reply-content");
                const timeEl = commentDiv.querySelector(".reply-time");

                contentEl.innerHTML = data.data.content;

                if (timeEl) {
                    let isEdited = false;
                    let rawTime = data.data.time;
                    if (rawTime.endsWith(" (edited)")) {
                        isEdited = true;
                        rawTime = rawTime.replace(" (edited)", "");
                    }
                    const timeAgo = formatTimeAgo(rawTime) + (isEdited ? " (edited)" : "");
                    timeEl.innerText = timeAgo;
                }
            } else {
                alert(data.message || "Failed to edit comment.");
            }
        })
        .catch(err => {
            console.error("Edit error:", err);
            alert("Something went wrong.");
        });
}

async function deleteReply(comment_id, reply_id) {
    try {
        const response = await fetch('http://127.0.0.1:8000/reply/deleteReply', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ comment_id, reply_id })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to delete comment');
        }
        if (data.data) {
            document.querySelector(`[data-id='${data.data.reply_id}']`).remove();
            const button = document.querySelector(`.reply-toggle[data-id="${comment_id}"]`);
            if (button) {
                const text = button.innerText.trim();
                const match = text.match(/\((\d+)\)/);
                if (match) {
                    let count = parseInt(match[1]) - 1;
                    button.innerHTML = `<i class="text-blue-400 fas fa-reply"></i> Reply (${formatCount(count)})`;
                }
            }

        }
    } catch (error) {
        console.error('Error deleting comment:', error.message);
    }
}

async function addVoteToReply(replyId, voteType) {
    try {
        const response = await fetch("http://localhost:8000/voteReply/addReplyVote", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                reply_id: replyId,
                user_id: sessionStorage.getItem("userId"),
                vote_type: voteType,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to add vote");
        }

        const responseData = await response.json();

        const upvoteIcon = document.querySelector(`.upvote-reply[data-id='${replyId}']`);
        const downvoteIcon = document.querySelector(`.downvote-reply[data-id='${replyId}']`);

        const upvoteCountEl = upvoteIcon?.nextElementSibling;
        const downvoteCountEl = downvoteIcon?.nextElementSibling;


        let upvoteCount = parseInt(upvoteCountEl?.textContent.trim() || 0);
        let downvoteCount = parseInt(downvoteCountEl?.textContent.trim() || 0);

        switch (responseData.data.message) {
            case "Upvote added.":
                upvoteCount++;
                upvoteIcon.classList.replace("fa-regular", "fa-solid");
                downvoteIcon.classList.replace("fa-solid", "fa-regular");
                break;
            case "Downvote added.":
                downvoteCount++;
                downvoteIcon.classList.replace("fa-regular", "fa-solid");
                upvoteIcon.classList.replace("fa-solid", "fa-regular");
                break;
            case "Upvote removed.":
                upvoteCount--;
                upvoteIcon.classList.replace("fa-solid", "fa-regular");
                break;
            case "Downvote removed.":
                downvoteCount--;
                downvoteIcon.classList.replace("fa-solid", "fa-regular");
                break;
            case "Vote updated from upvote to downvote.":
                upvoteCount--;
                downvoteCount++;
                upvoteIcon.classList.replace("fa-solid", "fa-regular");
                downvoteIcon.classList.replace("fa-regular", "fa-solid");
                break;
            case "Vote updated from downvote to upvote.":
                downvoteCount--;
                upvoteCount++;
                downvoteIcon.classList.replace("fa-solid", "fa-regular");
                upvoteIcon.classList.replace("fa-regular", "fa-solid");
                break;
        }

        if (upvoteCountEl) upvoteCountEl.textContent = `${formatCount(upvoteCount)}`;
        if (downvoteCountEl) downvoteCountEl.textContent = `${formatCount(downvoteCount)}`;

    } catch (error) {
        console.error("Error adding vote:", error);
    }
}

async function getReplyVote(replyId) {
    try {
        const response = await fetch("http://localhost:8000/voteReply/getReplyVote", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                reply_id: replyId,
                user_id: sessionStorage.getItem("userId"),
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to get vote");
        }

        const responseData = await response.json();

        const upvoteIcon = document.querySelector(`.upvote-reply[data-id='${replyId}']`);
        const downvoteIcon = document.querySelector(`.downvote-reply[data-id='${replyId}']`);

        const upvoteCountEl = upvoteIcon?.nextElementSibling;
        const downvoteCountEl = downvoteIcon?.nextElementSibling;


        if (responseData.data.vote_type === "upvote") {
            upvoteIcon.classList.replace("fa-regular", "fa-solid");
            downvoteIcon.classList.replace("fa-solid", "fa-regular");
        } else if (responseData.data.vote_type === "downvote") {
            downvoteIcon.classList.replace("fa-regular", "fa-solid");
            upvoteIcon.classList.replace("fa-solid", "fa-regular");
        }

        if (responseData.data) {
            upvoteCountEl.textContent = ` ${formatCount(responseData.data.upvotes)}`;
            downvoteCountEl.textContent = ` ${formatCount(responseData.data.downvotes)}`;
        }

    } catch (error) {
        console.error("Error getting vote:", error);
    }
}