window.addEventListener("DOMContentLoaded", function () {
    const postData = JSON.parse(localStorage.getItem("selectedPost"));
    if (!postData) return;

    const container = document.getElementById("post-container");

    const timestamp = new Date(postData.timestamp);
    const date = timestamp.toLocaleDateString();
    const time = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const editedBadge = postData.edited
        ? `<div class="absolute bottom-36 right-4 bg-yellow-500 text-black text-xs sm:text-sm px-2 py-0.5 rounded">Edited</div>`
        : "";

    const html = `
        <div class="w-full relative">
    <img src="${postData.image_url}" alt="Image" class="rounded-xl mb-3 sm:mb-4 w-full max-h-72 object-cover border-b">
    ${editedBadge}
    <h2 class="text-lg sm:text-xl font-bold mb-2 break-words px-6">${postData.title}</h2>
    <p class="text-gray-300 mb-4 text-sm sm:text-base leading-relaxed break-words px-6">
        ${postData.content}
    </p>
    <div class="flex flex-wrap justify-between items-center text-xs sm:text-sm text-gray-400 mb-4 px-6">
        <div class="break-words">
            Posted by <span class="text-blue-400 font-medium">@${postData.username}</span><br>
            <span class="text-gray-500">${date}, ${time}</span>
        </div>
        <div class="flex gap-3 mt-2 sm:mt-0">
            <span class="text-blue-400 hover:text-blue-300 text-base">
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
                <span class="text-cyan-400 text-sm sm:text-base">
                    <i class="fa-regular fa-eye"></i>
                </span>
                <span id="view-count">${postData.views}</span>
            </div>
            <div class="flex flex-col items-center">
                <span class="text-blue-400 text-sm sm:text-base">
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
                <span class="text-blue-400 hover:text-blue-300 text-sm sm:text-base">
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
        if (responseData.data === "upvote") {
            let count = document.getElementById("upvote-count").innerText;
            count = parseInt(count) + 1;
            document.getElementById("upvote-count").innerText = formatCount(count);
            document.getElementById("upvote-icon").classList.remove("fa-regular");
            document.getElementById("upvote-icon").classList.add("fa-solid");
            document.getElementById("downvote-icon").classList.remove("fa-solid");
            document.getElementById("downvote-icon").classList.add("fa-regular");
        } else if (responseData.data === "downvote") {
            let count = document.getElementById("downvote-count").innerText;
            count = parseInt(count) + 1;
            document.getElementById("downvote-count").innerText = formatCount(count);
            document.getElementById("downvote-icon").classList.remove("fa-regular");
            document.getElementById("downvote-icon").classList.add("fa-solid");
            document.getElementById("upvote-icon").classList.remove("fa-solid");
            document.getElementById("upvote-icon").classList.add("fa-regular");
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
            document.getElementById("followed-icon").classList.remove("fa-regular");
            document.getElementById("followed-icon").classList.add("fa-solid");
        }
        if (responseData.message === "Thread followed.") {
            let count = document.getElementById("followed-count").innerText;
            count = parseInt(count) + 1;
            document.getElementById("followed-count").innerText = formatCount(count);
            document.getElementById("followed-icon").classList.remove("fa-solid");
            document.getElementById("followed-icon").classList.add("fa-regular");
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