const showPost = document.getElementById("showPost");
const showFollowed = document.getElementById("showFollowed");
const showBookmark = document.getElementById("showBookmark");
const username = document.getElementById("username");
const bio = document.getElementById("bio");
const editProfile = document.getElementById("editProfile");
const profileModal = document.getElementById("editProfileModal");
const closeProfile = document.getElementById("close-profile");
const buttons = [showPost, showFollowed, showBookmark];
const confirmChanges = document.getElementById("confirmChanges");
const form = document.getElementById("editProfileForm");
const profilePicInput = document.getElementById("profilePic");
const previewImage = document.getElementById("previewImage");
const removeBtn = document.getElementById("removeProfilePic");
const defaultImage = "../assets/profile.png";
let imageChanged = false;
let imageRemoved = false;
const defaultBio = "Listening, learning, and maybe posting soon...";
const myDiv = document.getElementById("profile");
const usernameInput = document.getElementById("username");
let selectedPostId = null;
let selectedUserId = null;
let PostID = "";

usernameInput.addEventListener("input", function () {
    this.value = this.value.replace(/\s/g, "");
    if (this.value.length > 16) {
        this.value = this.value.slice(0, 16);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    localStorage.removeItem("selectedPost");
    localStorage.removeItem("userPosts");
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("id")) {
        getIdFromUrlAndClean();
    } else {
        getProfile();
        fetchUserPosts();
    }
})

buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
        buttons.forEach((b) => b.classList.remove("border-b"));
        btn.classList.add("border-b");
    });
});

editProfile.addEventListener("click", () => {
    previewImage.src = document.getElementById("profileImg").src || defaultImage;
    username.value = document.getElementById("profileUsername").innerText;
    if (document.getElementById("profileBio").innerText === "Listening, learning, and maybe posting soon...") {
        bio.value = "";
    } else {
        bio.value = document.getElementById("profileBio").innerText;
    }
    profileModal.classList.remove("hidden");
    profileModal.classList.add("flex");
    checkImageState();
});

closeProfile.addEventListener("click", () => {
    profileModal.classList.remove("flex");
    profileModal.classList.add("hidden");
});

function checkImageState() {
    if (!previewImage.src.includes("profile.png")) {
        removeBtn.classList.remove("hidden");
    } else {
        removeBtn.classList.add("hidden");
    }
}

profilePicInput.addEventListener("change", () => {
    const file = profilePicInput.files[0];
    if (file) {
        previewImage.src = URL.createObjectURL(file);
        imageChanged = true;
        imageRemoved = false;
        removeBtn.classList.remove("hidden");
    }
});

removeBtn.addEventListener("click", () => {
    previewImage.src = defaultImage;
    profilePicInput.value = "";
    imageChanged = false;
    imageRemoved = true;
    removeBtn.classList.add("hidden");
});

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const bio = document.getElementById("bio").value.trim();
    const profilePicFile = profilePicInput.files[0];
    const isDefaultImage = previewImage.src.includes("profile.png");

    const userId = sessionStorage.getItem("userId");
    if (!userId) return alert("User ID not found in session.");
    if (username === "") return alert("Username cannot be empty.");

    const formData = new FormData();
    formData.append("username", username);
    formData.append("bio", bio);
    if (!isDefaultImage && profilePicFile) {
        formData.append("profilePic", profilePicFile);
    }

    try {
        const res = await fetch("http://localhost:8000/profile/update", {
            method: "POST",
            body: formData,
            headers: {
                "user-id": userId,
            },
        });

        let result;
        try {
            result = await res.json();
        } catch (parseErr) {
            console.error("Failed to parse JSON:", parseErr);
            return alert("Invalid server response.");
        }

        if (res.ok) {
            alert("Profile updated successfully!");
            document.getElementById("profileBio").innerText = result.data.bio || defaultBio;
            document.getElementById("profileUsername").innerText = result.data.username;
            document.getElementById("profileImg").src = result.data.img || defaultImage;
            sessionStorage.setItem("username", result.data.username);
        } else {
            alert(result.details || "Update failed.");
        }
    } catch (err) {
        
    }
    profileModal.classList.remove("flex");
    profileModal.classList.add("hidden");
});

window.addEventListener("DOMContentLoaded", checkImageState);

async function getProfile() {
    try {
        const userId = sessionStorage.getItem("userId");
        const response = await fetch("http://localhost:8000/profile/get", {
            method: "GET",
            headers: {
                "user-id": userId,
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.data !== "") {
            document.getElementById("follow-user").dataset.userId = data.data.user_id;
            document.getElementById("profileUsername").innerText = data.data.username;
            document.getElementById("profileBio").innerText = data.data.bio || defaultBio;
            document.getElementById("followers-count").innerText = formatCount(data.data.followers);
            document.getElementById("following-count").innerText = formatCount(data.data.following);
            document.getElementById("reputation-count").innerText = formatCount(data.data.reputation);
            document.getElementById("posts-count").innerText = formatCount(data.data.total_posts);
            document.getElementById("upvotes-count").innerText = formatCount(data.data.total_upvotes);
            document.getElementById("downvotes-count").innerText = formatCount(data.data.total_downvotes);
            document.getElementById("view-count").innerText = formatCount(data.data.total_views);
            document.getElementById("bookmark-count").innerText = formatCount(data.data.total_bookmarks);
            if (data.data.follower_ids && data.data.follower_ids.includes(sessionStorage.getItem("userId"))) {
                document.getElementById("follow-user").innerText = "Unfollow";
            } else {
                document.getElementById("follow-user").innerText = "Follow";
            }
            if (data.data.img) {
                document.getElementById("profileImg").src = data.data.img;
            } else {
                document.getElementById("profileImg").src = defaultImage;
            }
            myDiv.id = data.data.user_id;
            if (myDiv.id === sessionStorage.getItem("userId")) {
                document.getElementById("followDiv").classList.remove("flex");
                document.getElementById("followDiv").classList.add("hidden");
                document.getElementById("editDiv").classList.remove("hidden");
                document.getElementById("editDiv").classList.add("flex");
            } else {
                document.getElementById("followDiv").classList.remove("hidden");
                document.getElementById("followDiv").classList.add("flex");
                document.getElementById("editDiv").classList.remove("flex");
                document.getElementById("editDiv").classList.add("hidden");
            }
        }

    } catch (error) {
        console.error("Error fetching profile:", error);
    }
}

document.getElementById("addPost").addEventListener("click", () => {
    const modal = document.getElementById("postModal");
    modal.classList.remove("hidden");
    modal.classList.add("flex");
});

document.getElementById("close-post").addEventListener("click", () => {
    const modal = document.getElementById("postModal");
    modal.classList.add("hidden");
    modal.classList.remove("flex");
});

function displayPosts(postList) {
    const display = document.getElementById("display");
    display.innerHTML = "";
    const pinnedPosts = [];
    const nonPinnedPosts = [];

    postList.forEach(post => {
        if (post.is_pinned === "True") {
            pinnedPosts.push(post);
        } else {
            nonPinnedPosts.push(post);
        }
    });

    const sortByTimestampDesc = (a, b) => new Date(b.timestamp) - new Date(a.timestamp);
    nonPinnedPosts.sort(sortByTimestampDesc);
    pinnedPosts.sort(sortByTimestampDesc);

    [...nonPinnedPosts].reverse().forEach(post => {
        const card = createPostCard(post);
        display.prepend(card);
    });

    [...pinnedPosts].reverse().forEach(post => {
        const card = createPostCard(post);
        display.prepend(card);
    });
}

function createPostCard(postData) {
    const imageUrl = postData.image_url ? postData.image_url : "../assets/post.png";

    const timestamp = new Date(postData.timestamp);
    const date = timestamp.toLocaleDateString();
    const time = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const sessionUserId = sessionStorage.getItem("userId");

    const postCard = document.createElement("div");
    postCard.id = postData.post_id;
    postCard.setAttribute("data-user-id", postData.user_id);
    postCard.className = "w-72 h-fit rounded-xl shadow-lg overflow-hidden flex flex-col border-2 border-black cursor-pointer";

    postCard.onclick = () => {
        localStorage.setItem("selectedPost", JSON.stringify(postData));
        window.location.href = "post.html";
    };

    postCard.innerHTML = `
        <div class="relative w-full h-48 overflow-hidden border-b border-slate-950">
            <img src="${imageUrl}" alt="Post Image" class="w-full h-full object-cover" />
            ${postData.is_pinned === "True" && postData.user_id === sessionUserId
            ? `<div class="absolute top-2 left-2 bg-slate-950 text-white rounded-full p-1 shadow">
                    <i class="fa-solid fa-thumbtack text-xs"></i>
                </div>`
            : ""}
            ${postData.is_locked === "True" && postData.user_id === sessionUserId && postData.is_pinned === "True"
            ? `<div class="absolute top-2 left-12 bg-slate-950 text-white rounded-full p-1 shadow">
                    <i class="fa-solid fa-lock text-xs"></i>
                </div>`
            : ""}
            ${postData.is_locked === "True" && postData.user_id === sessionUserId && postData.is_pinned === "False"
            ? `<div class="absolute top-2 left-2 bg-slate-950 text-white rounded-full p-1 shadow">
                    <i class="fa-solid fa-lock text-xs"></i>
                </div>`
            : ""}
            ${postData.user_id === sessionUserId || postData.user_id !== sessionUserId
            ? `<div class="absolute top-2 right-2 z-50">
                    <span onclick="event.stopPropagation(); toggleMenu('${postData.post_id}')" class="text-white text-sm px-2 py-1 rounded-full bg-slate-950 bg-opacity-40 hover:bg-opacity-60 cursor-pointer">
                        <i class="fa-solid fa-ellipsis-vertical"></i>
                    </span>
                    <div id="menu-${postData.post_id}" class="hidden absolute right-0 mt-1 w-36 bg-slate-900 text-gray-200 rounded-md shadow-lg z-50 overflow-hidden border border-gray-700 text-xs">
                        ${postData.user_id === sessionUserId
                ? `<span onclick="event.stopPropagation(); handleMenuAction('edit', '${postData.post_id}', '${postData.user_id}')" class="flex items-center gap-2 w-full px-3 py-2 hover:bg-gray-700 cursor-pointer">
                                <i class="fa-solid fa-pen-to-square text-blue-400 text-xs"></i> Edit
                            </span>
                            <span onclick="event.stopPropagation(); handleMenuAction('delete', '${postData.post_id}', '${postData.user_id}')" class="flex items-center gap-2 w-full px-3 py-2 hover:bg-gray-700 cursor-pointer">
                                <i class="fa-solid fa-trash text-red-400 text-xs"></i> Delete
                            </span>
                            <span onclick="event.stopPropagation(); handleMenuAction('${postData.is_pinned === "True" ? "unpin" : "pin"}', '${postData.post_id}', '${postData.user_id}')" class="flex items-center gap-2 w-full px-3 py-2 hover:bg-gray-700 cursor-pointer">
                                <i class="fa-solid fa-thumbtack text-yellow-400 text-xs"></i> ${postData.is_pinned === "True" ? "Unpin" : "Pin"}
                            </span>
                            <span onclick="event.stopPropagation(); handleMenuAction('${postData.is_locked === "True" ? "unblock" : "block"}', '${postData.post_id}', '${postData.user_id}')" class="flex items-center gap-2 w-full px-3 py-2 hover:bg-gray-700 cursor-pointer">
                                <i class="fa-solid fa-comment-slash text-purple-400 text-xs"></i> ${postData.is_locked === "True" ? "Unblock" : "Block"} Comment
                            </span>`
                : `<span onclick="event.stopPropagation(); handleMenuAction('remove', '${postData.post_id}', '${postData.user_id}')" class="flex items-center gap-2 w-full px-3 py-2 hover:bg-gray-700 cursor-pointer">
                                <i class="fa-solid fa-trash text-yellow-400 text-xs"></i> Remove
                            </span>
                            <span onclick="event.stopPropagation(); handleMenuAction('report', '${postData.post_id}', '${postData.user_id}')" class="flex items-center gap-2 w-full px-3 py-2 hover:bg-gray-700 cursor-pointer">
                                <i class="fa-solid fa-flag text-red-300 text-xs"></i> Report
                            </span>`}
                    </div>
               </div>`
            : ""}
        </div>
        <div class="flex flex-col justify-between p-4 flex-grow bg-slate-950">
            <div>
                <h4 class="text-base font-semibold text-blue-400 hover:text-blue-500 transition leading-snug line-clamp-2">
                    ${postData.title}
                </h4>
                <p class="text-xs text-gray-400 mt-2 line-clamp-4 leading-relaxed">
                    ${postData.content}
                </p>
                <p class="text-xs text-gray-400 mt-1 flex">
                    <span class="mr-1 text-gray-400 shrink-0">Category:</span>
                    <span class="text-white font-medium whitespace-nowrap overflow-hidden text-ellipsis inline-block max-w-[160px]">
                        ${postData.category_name}
                    </span>
                </p>
                <p class="text-xs text-gray-400 mt-1 flex">
                    <span class="mr-1 text-gray-400 shrink-0">Tags:</span>
                    <span class="text-white font-medium whitespace-nowrap overflow-hidden text-ellipsis inline-block max-w-[160px]">
                        ${postData.tags}
                    </span>
                </p>
                <p class="text-xs text-gray-400 mt-2">Posted by 
                    <span class="text-white font-medium">${postData.username}</span> 
                    on <span class="text-white">${date}</span> at <span class="text-white">${time}</span>
                </p>
            </div>
            <div class="mt-4 flex justify-between text-gray-300 border-t border-gray-600 pt-3">
    <span class="flex items-center gap-1 text-sm hover:text-yellow-300 cursor-pointer">
        <i class="fa-solid fa-bookmark text-yellow-300 text-xs"></i><span>${formatCount(postData.bookmark_count)}</span>
    </span>
    <span class="flex items-center gap-1 text-sm cursor-pointer">
        <i class="fa-solid fa-share-alt text-lime-300 text-xs"></i><span>${formatCount(postData.shared)}</span>
    </span>
    <span class="flex items-center gap-1 text-sm cursor-pointer">
        <i class="fa-solid fa-square-plus text-purple-500 text-xs"></i><span>${formatCount(postData.followed)}</span>
    </span>
    <span class="flex items-center gap-1 text-sm cursor-pointer">
        <i class="fa-solid fa-flag text-red-600 text-xs"></i>
    </span>
</div>
<div class="flex justify-between text-sm text-gray-300 mt-4 border-t border-gray-600 pt-3">
    <div class="flex items-center gap-1 text-xs">
        <i class="fa-solid fa-thumbs-up text-green-400"></i><span>${formatCount(postData.upvotes)}</span>
    </div>
    <div class="flex items-center gap-1 text-xs">
        <i class="fa-solid fa-thumbs-down text-red-400"></i><span>${formatCount(postData.downvotes)}</span>
    </div>
    <div class="flex items-center gap-1 text-xs">
        <i class="fa-solid fa-eye text-emerald-400"></i><span>${formatCount(postData.views)}</span>
    </div>
    <div class="flex items-center gap-1 text-xs">
        <i class="fa-solid fa-comment text-blue-400"></i><span>${formatCount(postData.comment_count)}</span>
    </div>
</div>
            </div>
        </div>
    `;

    return postCard;
}

function toggleMenu(postId) {
    const menu = document.getElementById(`menu-${postId}`);
    document.querySelectorAll("[id^='menu-']").forEach(m => {
        if (m !== menu) m.classList.add("hidden");
    });
    menu.classList.toggle("hidden");
}

function handleMenuAction(action, postId, userId) {
    selectedPostId = postId;
    selectedUserId = userId;
    const menu = document.getElementById(`menu-${postId}`);
    menu.classList.add("hidden");
    switch (action) {
        case 'edit':
            openEditPostModal(postId);
            break;
        case 'delete':
            deletePost(postId);
            break;
        case 'pin':
            pinUnpinPost(postId, "True");
            break;
        case 'unpin':
            pinUnpinPost(postId, "False");
            break;
        case 'block':
            blockUnblockPost(postId, "True");
            break;
            break;
        case 'unblock':
            blockUnblockPost(postId, "False");
            break;
    }
}

const postForm = document.getElementById("postForm");
const postImageInput = document.getElementById("postImage");

document.getElementById("tags").addEventListener("input", (e) => {
    e.target.value = e.target.value.replace(/\s/g, '');
});

postForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("postTitle").value.trim();
    const content = document.getElementById("postContent").value.trim();
    const tags = document.getElementById("tags").value.trim();
    const category = document.getElementById("category").value;
    const postImageFile = postImageInput.files[0];

    const userId = sessionStorage.getItem("userId");
    if (!userId) return alert("User ID not found in session.");
    if (!title || !content || !category) return alert("Please fill in all required fields.");

    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);
    formData.append("category", category);
    formData.append("tags", tags);
    formData.append("user_id", userId);

    if (postImageFile) {
        formData.append("postImage", postImageFile);
    }

    try {
        const res = await fetch("http://localhost:8000/post/addPost", {
            method: "POST",
            body: formData,
        });

        let result;
        try {
            result = await res.json();
        } catch (parseErr) {
            console.error("Failed to parse JSON:", parseErr);
            return alert("Invalid server response.");
        }

        if (res.ok) {
            alert("Post created successfully!");
            postForm.reset();
            document.getElementById("postModal").classList.remove("flex");
            document.getElementById("postModal").classList.add("hidden");
        } else {
            alert(result.details || "Post creation failed.");
        }

    } catch (err) {
        console.error("Error during fetch:", err);
        alert("Something went wrong: " + (err.details || err.message));
    }
});

async function fetchUserPosts() {
    const userId = sessionStorage.getItem("userId");
    if (!userId) return alert("User ID not found in session.");

    try {
        const response = await fetch("http://localhost:8000/post/getPost", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_id: userId })
        });

        const data = await response.json();
        if (data.data !== "") {
            localStorage.setItem("userPosts", JSON.stringify(data.data));
            const storedPosts = JSON.parse(localStorage.getItem("userPosts"));
            displayPosts(storedPosts);
        }
    } catch (error) {
        console.error("Error fetching posts:", error);
    }
}

function pinPost(postId) {
    const userId = sessionStorage.getItem("userId");
    let posts = JSON.parse(localStorage.getItem('userPosts')) || [];

    let post = posts.find(p => p.post_id === postId && p.user_id === userId);

    if (post) {
        post.is_pinned = "True";
        localStorage.setItem("userPosts", JSON.stringify(posts));
        const storedPosts = JSON.parse(localStorage.getItem("userPosts"));
        displayPosts(storedPosts);
    }
}

function unpinPost(postId) {
    const userId = sessionStorage.getItem("userId");
    let posts = JSON.parse(localStorage.getItem('userPosts')) || [];

    let post = posts.find(p => p.post_id === postId && p.user_id === userId);

    if (post) {
        post.is_pinned = "False";
        localStorage.setItem("userPosts", JSON.stringify(posts));
        const storedPosts = JSON.parse(localStorage.getItem("userPosts"));
        displayPosts(storedPosts);
    }
}

function blockComments(postId) {
    const userId = sessionStorage.getItem("userId");
    let posts = JSON.parse(localStorage.getItem('userPosts')) || [];

    let post = posts.find(p => p.post_id === postId && p.user_id === userId);

    if (post) {
        post.is_locked = "True";
        localStorage.setItem("userPosts", JSON.stringify(posts));
        const storedPosts = JSON.parse(localStorage.getItem("userPosts"));
        displayPosts(storedPosts);
    }
}

function unblockComments(postId) {
    const userId = sessionStorage.getItem("userId");
    let posts = JSON.parse(localStorage.getItem('userPosts')) || [];

    let post = posts.find(p => p.post_id === postId && p.user_id === userId);

    if (post) {
        post.is_locked = "False";
        localStorage.setItem("userPosts", JSON.stringify(posts));
        const storedPosts = JSON.parse(localStorage.getItem("userPosts"));
        displayPosts(storedPosts);
    }
}

async function pinUnpinPost(postId, action) {
    try {
        const response = await fetch("http://localhost:8000/post/pinUnpin", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ post_id: postId, is_pinned: action, is_locked: action })
        });

        const data = await response.json();
        if (data.message) {
            if (action === "True") {
                pinPost(postId);
            } else {
                unpinPost(postId);
            }
        }
    } catch (error) {
        console.error("Error fetching posts:", error);
    }
}

async function blockUnblockPost(postId, action) {
    try {
        const response = await fetch("http://localhost:8000/post/blockUnblock", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ post_id: postId, is_pinned: action, is_locked: action })
        });

        const data = await response.json();
        if (data.message) {
            if (action === "True") {
                blockComments(postId);
            } else {
                unblockComments(postId);
            }
        }
    } catch (error) {
        console.error("Error fetching posts:", error);
    }
}

async function deletePost(postId) {
    const userId = sessionStorage.getItem("userId");
    let username = sessionStorage.getItem("username");
    try {
        const response = await fetch("http://localhost:8000/post/delete", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ post_id: postId, user_id: userId, username: username })
        });

        const data = await response.json();
        if (data.data && data.data.length > 0) {
            const deletedPostId = data.data[0];
            let posts = JSON.parse(localStorage.getItem('userPosts')) || [];
            posts = posts.filter(p => p.post_id !== deletedPostId);
            localStorage.setItem('userPosts', JSON.stringify(posts));
            const storedPosts = JSON.parse(localStorage.getItem("userPosts"));
            displayPosts(storedPosts);
            let count = document.getElementById("reputation-count").innerText;
            let correctCount = parseInt(count) - 5;
            document.getElementById("reputation-count").innerText = correctCount;
        }
    } catch (error) {
        console.error("Error fetching posts:", error);
    }
}

const openEditPostModal = (postId) => {
    document.getElementById("editPostModal").classList.remove("hidden");
    document.getElementById("editPostModal").classList.add("flex");

    const userPosts = JSON.parse(localStorage.getItem("userPosts"));
    if (!userPosts) return alert("No posts found.");

    const post = userPosts.find(p => p.post_id === postId);
    if (!post) return alert("Post not found.");

    document.getElementById("editPostTitle").value = post.title || "";
    document.getElementById("editPostContent").value = post.content || "";
    document.getElementById("editTags").value = post.tags || "";
    const categorySelect = document.getElementById("editCategory");
    const categoryText = post.category_name;
    for (let option of categorySelect.options) {
        if (option.text.trim().toLowerCase() === categoryText.trim().toLowerCase()) {
            categorySelect.value = option.value;
            break;
        }
    }
    if (post.image_url) {
        document.getElementById("editPostImagePreview").src = post.image_url;
        document.getElementById("editImagePreviewContainer").classList.remove("hidden");
        document.getElementById("editImagePreviewContainer").classList.add("flex");
        document.getElementById("editImageInputContainer").classList.add("hidden");
    } else {
        document.getElementById("editImagePreviewContainer").classList.remove("flex");
        document.getElementById("editImagePreviewContainer").classList.add("hidden");
        document.getElementById("editImageInputContainer").classList.remove("hidden");
    }
    PostID = postId;
};

document.getElementById("removeEditImageUrl").addEventListener("click", () => {
    document.getElementById("editImagePreviewContainer").classList.remove("flex");
    document.getElementById("editImagePreviewContainer").classList.add("hidden");
    document.getElementById("editImageInputContainer").classList.remove("hidden");
    document.getElementById("editPostImagePreview").src = "";
    document.getElementById("editPostImage").value = "";
});

const closeEditPostModal = () => {
    document.getElementById("editPostModal").classList.remove("flex");
    document.getElementById("editPostModal").classList.add("hidden");
    PostID = "";
};

document.getElementById("close-edit-post").addEventListener("click", closeEditPostModal);

document.getElementById("editPostForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("editPostTitle").value.trim();
    const content = document.getElementById("editPostContent").value.trim();
    const tags = document.getElementById("editTags").value.trim();
    const category = document.getElementById("editCategory").value;
    const postImageFile = document.getElementById("editPostImage").files[0];

    if (!title || !content || !category) return alert("Please fill in all required fields.");

    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);
    formData.append("category", category);
    formData.append("tags", tags);
    formData.append("post_id", PostID);

    if (postImageFile) {
        formData.append("postImage", postImageFile);
    } else {
        const previewSrc = document.getElementById("editPostImagePreview").getAttribute("src");
        if (previewSrc) {
            formData.append("previewImage", previewSrc);
        }
    }

    try {
        const res = await fetch("http://localhost:8000/post/editPost", {
            method: "POST",
            body: formData,
        });

        let result;
        try {
            result = await res.json();
        } catch (parseErr) {
            console.error("Failed to parse JSON:", parseErr);
            return alert("Invalid server response.");
        }

        if (res.ok) {
            alert("Post updated successfully!");
            document.getElementById("editPostForm").reset();
            document.getElementById("editPostModal").classList.remove("flex");
            document.getElementById("editPostModal").classList.add("hidden");
        } else {
            alert(result.details || "Post update failed.");
        }

    } catch (err) {
       
    }
    PostID = "";
});

async function fetchUserBookmark() {
    const userId = sessionStorage.getItem("userId");
    if (!userId) return alert("User ID not found in session.");

    try {
        const response = await fetch("http://localhost:8000/post/getBookmark", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_id: userId })
        });

        const data = await response.json();
        if (data.data !== "") {
            localStorage.setItem("bookmarkPosts", JSON.stringify(data.data));
            const storedPosts = JSON.parse(localStorage.getItem("bookmarkPosts"));
            displayPosts(storedPosts);
        }
    } catch (error) {
        console.error("Error fetching posts:", error);
    }
}

async function fetchUserFollowedThread() {
    const userId = sessionStorage.getItem("userId");
    if (!userId) return alert("User ID not found in session.");

    try {
        const response = await fetch("http://localhost:8000/post/getFollowedThread", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_id: userId })
        });

        const data = await response.json();
        if (data.data !== "") {
            localStorage.setItem("FollowedThread", JSON.stringify(data.data));
            const storedPosts = JSON.parse(localStorage.getItem("FollowedThread"));
            displayPosts(storedPosts);
        }
    } catch (error) {
        console.error("Error fetching posts:", error);
    }
}

showPost.addEventListener("click", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("id")) {
        try {
            const response = await fetch("http://localhost:8000/post/getPost", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ user_id: urlParams.get("id") })
            });

            const data = await response.json();
            if (data.data !== "") {
                localStorage.setItem("userPosts", JSON.stringify(data.data));
                const storedPosts = JSON.parse(localStorage.getItem("userPosts"));
                displayPosts(storedPosts);
            }
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    } else {
        fetchUserPosts();
    }
});

showBookmark.addEventListener("click", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("id")) {
        try {
            const response = await fetch("http://localhost:8000/post/getBookmark", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ user_id: urlParams.get("id") })
            });

            const data = await response.json();
            if (data.data !== "") {
                localStorage.setItem("bookmarkPosts", JSON.stringify(data.data));
                const storedPosts = JSON.parse(localStorage.getItem("bookmarkPosts"));
                displayPosts(storedPosts);
            }
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    } else {
        fetchUserBookmark();
    }
});

showFollowed.addEventListener("click", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("id")) {
        try {
            const response = await fetch("http://localhost:8000/post/getFollowedThread", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ user_id: urlParams.get("id") })
            });

            const data = await response.json();
            if (data.data !== "") {
                localStorage.setItem("FollowedThread", JSON.stringify(data.data));
                const storedPosts = JSON.parse(localStorage.getItem("FollowedThread"));
                displayPosts(storedPosts);
            }
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    } else {
        fetchUserFollowedThread();
    }
});

function formatCount(num) {
    if (num >= 1_000_000) {
        return (num / 1_000_000).toFixed(1).replace(/\.0$/, '') + 'M';
    } else if (num >= 1_000) {
        return (num / 1_000).toFixed(1).replace(/\.0$/, '') + 'k';
    } else {
        return num.toString();
    }
}

async function getIdFromUrlAndClean() {
    const url = new URL(window.location.href);
    const id = url.searchParams.get("id");
    try {
        const response = await fetch("http://localhost:8000/post/getPost", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_id: id })
        });

        const data = await response.json();
        if (data.data !== "") {
            localStorage.setItem("userPosts", JSON.stringify(data.data));
            const storedPosts = JSON.parse(localStorage.getItem("userPosts"));
            displayPosts(storedPosts);
        }
    } catch (error) {
        console.error("Error fetching posts:", error);
    }
    try {
        const response = await fetch("http://localhost:8000/profile/get", {
            method: "GET",
            headers: {
                "user-id": id,
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.data !== "") {
            document.getElementById("follow-user").dataset.userId = data.data.user_id;
            document.getElementById("message-user").dataset.userId = data.data.user_id;
            document.getElementById("message-user").dataset.username = data.data.username;
            document.getElementById("message-user").dataset.img = data.data.img;
            document.getElementById("profileUsername").innerText = data.data.username;
            document.getElementById("profileBio").innerText = data.data.bio || defaultBio;
            document.getElementById("followers-count").innerText = formatCount(data.data.followers);
            document.getElementById("following-count").innerText = formatCount(data.data.following);
            document.getElementById("reputation-count").innerText = formatCount(data.data.reputation);
            document.getElementById("posts-count").innerText = formatCount(data.data.total_posts);
            document.getElementById("upvotes-count").innerText = formatCount(data.data.total_upvotes);
            document.getElementById("downvotes-count").innerText = formatCount(data.data.total_downvotes);
            document.getElementById("view-count").innerText = formatCount(data.data.total_views);
            document.getElementById("bookmark-count").innerText = formatCount(data.data.total_bookmarks);
            if (data.data.follower_ids && data.data.follower_ids.includes(sessionStorage.getItem("userId"))) {
                document.getElementById("follow-user").innerText = "Unfollow";
            } else {
                document.getElementById("follow-user").innerText = "Follow";
            }
            if (data.data.img) {
                document.getElementById("profileImg").src = data.data.img;
            } else {
                document.getElementById("profileImg").src = defaultImage;
            }
            myDiv.id = data.data.user_id;
            if (myDiv.id === sessionStorage.getItem("userId")) {
                document.getElementById("followDiv").classList.remove("flex");
                document.getElementById("followDiv").classList.add("hidden");
                document.getElementById("editDiv").classList.remove("hidden");
                document.getElementById("editDiv").classList.add("flex");
            } else {
                document.getElementById("followDiv").classList.remove("hidden");
                document.getElementById("followDiv").classList.add("flex");
                document.getElementById("editDiv").classList.remove("flex");
                document.getElementById("editDiv").classList.add("hidden");
            }
        }

    } catch (error) {
        console.error("Error fetching profile:", error);
    }
    return id;
}

document.getElementById("follow-user").addEventListener("click", async (event) => {
    event.preventDefault();
    const follow_id = document.getElementById("follow-user").getAttribute("data-user-id");
    const user_id = sessionStorage.getItem("userId");
    if (document.getElementById("follow-user").innerText === "Follow") {
        sendFollowRequest(user_id, follow_id);
    } else {
        sendUnfollowRequest(user_id, follow_id);
    }
});

document.getElementById("message-user").addEventListener("click", async (event) => {
    event.preventDefault();
    const userId = document.getElementById("message-user").dataset.userId;
    const username = encodeURIComponent(document.getElementById("message-user").dataset.username);
    const img = encodeURIComponent(document.getElementById("message-user").dataset.img);
    const url = `./chat.html?userId=${userId}&username=${username}&img=${img}`;
    window.location.href = url;
});

async function sendFollowRequest(userId, followId) {
    try {
        const response = await fetch("http://localhost:8000/follow/follow", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                follow_id: followId
            })
        });

        const result = await response.json();
        if (result.message) {
            let count = document.getElementById("followers-count").innerText;
            count = parseInt(count) + 1;
            document.getElementById("followers-count").innerText = formatCount(count);
            document.getElementById("follow-user").innerText = "Unfollow";
        }
    } catch (error) {
        console.error("Error while following:", error);
    }
}

async function sendUnfollowRequest(userId, followId) {
    try {
        const response = await fetch("http://localhost:8000/follow/unfollow", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                follow_id: followId
            })
        });

        const result = await response.json();
        if (result.message) {
            let count = document.getElementById("followers-count").innerText;
            count = parseInt(count) - 1;
            document.getElementById("followers-count").innerText = formatCount(count);
            document.getElementById("follow-user").innerText = "Follow";
        }
    } catch (error) {
        console.error("Error while unfollowing:", error);
    }
}
