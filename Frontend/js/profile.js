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

usernameInput.addEventListener("input", function () {
    this.value = this.value.replace(/\s/g, "");
    if (this.value.length > 16) {
        this.value = this.value.slice(0, 16);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    getProfile();
})

buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
        buttons.forEach((b) => b.classList.remove("border-b"));
        btn.classList.add("border-b");
    });
});

editProfile.addEventListener("click", () => {
    username.value = document.getElementById("profileUsername").innerText;
    if (document.getElementById("profileBio").innerText === "Listening, learning, and maybe posting soon...") {
        bio.value = "";
    } else {
        bio.value = document.getElementById("profileBio").innerText;
    }
    profileModal.classList.remove("hidden");
    profileModal.classList.add("flex");
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

    if (!userId) {
        alert("User ID not found in session.");
        return;
    }

    if (username === "") {
        alert("Username cannot be empty.");
        return;
    }

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
        e.preventDefault();
        const result = await res.json();
        if (res.ok) {
            alert("Profile updated successfully!");
            document.getElementById("profileBio").innerText = result.data.bio || defaultBio;
            document.getElementById("profileUsername").innerText = result.data.username;
            document.getElementById("profileImg").src = result.data.img || defaultImage;
            if (result.data.username !== sessionStorage.getItem("username")) {
                sessionStorage.setItem("username", result.data.username);
            }
        } else {
            alert(result.details || "Update failed.");
        }
        profileModal.classList.remove("flex");
        profileModal.classList.add("hidden");
        e.preventDefault();
    } catch (err) {
        console.error(err);
        alert("Something went wrong!", err.details||err.message);
    }
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
            document.getElementById("profileUsername").innerText = sessionStorage.getItem("username");
            document.getElementById("profileBio").innerText = data.data.bio || defaultBio;
            document.getElementById("followers-count").innerText = data.data.followers;
            document.getElementById("following-count").innerText = data.data.following;
            document.getElementById("reputation-count").innerText = data.data.reputation;
            document.getElementById("posts-count").innerText = data.data.total_posts;
            document.getElementById("upvotes-count").innerText = data.data.total_upvotes;
            document.getElementById("downvotes-count").innerText = data.data.total_downvotes;
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

document.getElementById("postImage").addEventListener("change", function () {
    const preview = document.getElementById("imagePreview");
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.classList.remove("hidden");
        };
        reader.readAsDataURL(file);
    } else {
        preview.classList.add("hidden");
        preview.src = "";
    }
});

function addPostToDisplay(postData) {
    const display = document.getElementById("display");

    const postCard = document.createElement("div");
    postCard.className = "w-72 h-[510px] bg-gray-700 rounded-xl shadow-lg overflow-hidden flex flex-col border-2 cursor-pointer";
    postCard.onclick = () => {
        localStorage.setItem("selectedPost", JSON.stringify(postData));
        window.location.href = "post-details.html"; // ya jo page tu chahta hai
    };

    postCard.innerHTML = `
        <div class="w-full h-48 overflow-hidden">
            <img src="${postData.image}" alt="Post Image" class="w-full h-full object-cover" />
        </div>
        <div class="flex flex-col justify-between p-4 flex-grow">
            <div>
                <h4 class="text-base font-semibold text-blue-400 hover:text-blue-500 transition leading-snug line-clamp-2">
                    ${postData.title}
                </h4>
                <p class="text-xs text-gray-400 mt-2 line-clamp-4 leading-relaxed">
                    ${postData.description}
                </p>
                <p class="text-xs text-gray-400 mt-1 flex">
                    <span class="mr-1 text-gray-400 shrink-0">Category:</span>
                    <span class="text-white font-medium whitespace-nowrap overflow-hidden text-ellipsis inline-block max-w-[160px]">
                        ${postData.category}
                    </span>
                </p>
                <p class="text-xs text-gray-400 mt-1 flex">
                    <span class="mr-1 text-gray-400 shrink-0">Tags:</span>
                    <span class="text-white font-medium whitespace-nowrap overflow-hidden text-ellipsis inline-block max-w-[160px]">
                        ${postData.tags}
                    </span>
                </p>
                <p class="text-xs text-gray-400 mt-2">Posted by 
                    <span class="text-white font-medium">${postData.author}</span> on ${postData.date}
                </p>
            </div>
            <div class="mt-4 flex justify-between text-gray-300 border-t border-gray-600 pt-3">
                <button class="flex items-center gap-1 text-sm hover:text-yellow-300">
                    <i class="fa-regular fa-bookmark text-yellow-300 text-xs"></i><span>${postData.bookmarks}</span>
                </button>
                <button class="flex items-center gap-1 text-sm">
                    <i class="fa-solid fa-share-alt text-lime-300 text-xs"></i><span>${postData.shares}</span>
                </button>
                <button class="flex items-center gap-1 text-sm">
                    <i class="fa-regular fa-square-plus text-purple-500 text-xs"></i><span>${postData.saves}</span>
                </button>
                <button class="flex items-center gap-1 text-sm">
                    <i class="fa-regular fa-flag text-red-300 text-xs"></i>
                </button>
            </div>
            <div class="flex justify-between text-sm text-gray-300 mt-4 border-t border-gray-600 pt-3">
                <div class="flex items-center gap-1 text-xs">
                    <i class="fa-solid fa-up-long text-green-400"></i><span>${postData.upvotes}</span>
                </div>
                <div class="flex items-center gap-1 text-xs">
                    <i class="fa-solid fa-down-long text-red-400"></i><span>${postData.downvotes}</span>
                </div>
                <div class="flex items-center gap-1 text-xs">
                    <i class="fa-regular fa-eye text-emerald-400"></i><span>${postData.views}</span>
                </div>
                <div class="flex items-center gap-1 text-xs">
                    <i class="fa-regular fa-comment text-blue-400"></i><span>${postData.comments}</span>
                </div>
            </div>
        </div>
    `;

    display.appendChild(postCard);
}

const postsData = [
    {
        title: "Clean Code Practices Every Developer Should Follow",
        description: "Discover the top habits and principles of writing clean, maintainable code used by professional developers.",
        author: "codeGuru",
        date: "April 7, 2025",
        category: "Web Development",
        tags: "Clean Code, Best Practices, JavaScript",
        image: "../assets/code.jpg",
        bookmarks: 43,
        shares: 20,
        saves: 30,
        upvotes: 75,
        downvotes: 5,
        views: 900,
        comments: 8
    },
    {
        title: "Mastering React in 30 Days: Roadmap Included",
        description: "Learn how to become a React developer from scratch with this 30-day learning plan.",
        author: "devMaster",
        date: "March 28, 2025",
        category: "Frontend",
        tags: "React, JavaScript, Web App",
        image: "../assets/react.png",
        bookmarks: 80,
        shares: 54,
        saves: 45,
        upvotes: 100,
        downvotes: 3,
        views: 1200,
        comments: 10
    },
    {
        title: "Building Your First REST API with Node.js",
        description: "Step-by-step tutorial to build and test a fully functional REST API using Express.",
        author: "apiKing",
        date: "April 1, 2025",
        category: "Backend",
        tags: "Node.js, REST, API, Express",
        image: "../assets/nodeapi.png",
        bookmarks: 64,
        shares: 33,
        saves: 29,
        upvotes: 88,
        downvotes: 6,
        views: 950,
        comments: 5
    },
    {
        title: "Top 10 VS Code Extensions for Developers",
        description: "Boost your coding efficiency with these must-have extensions for Visual Studio Code.",
        author: "toolBox",
        date: "March 18, 2025",
        category: "Tools",
        tags: "VS Code, Productivity, Extensions",
        image: "../assets/vscode.jpg",
        bookmarks: 22,
        shares: 11,
        saves: 15,
        upvotes: 60,
        downvotes: 1,
        views: 700,
        comments: 2
    },
    {
        title: "Understanding JavaScript Closures with Examples",
        description: "Closures are a fundamental concept. This post breaks them down with simple code samples.",
        author: "jsWizard",
        date: "April 4, 2025",
        category: "JavaScript",
        tags: "Closures, Scope, JavaScript",
        image: "../assets/js-closure.png",
        bookmarks: 55,
        shares: 18,
        saves: 22,
        upvotes: 70,
        downvotes: 2,
        views: 800,
        comments: 6
    },
    {
        title: "Design Tips for a Clean UI in Web Projects",
        description: "Good UI is half the product. Here are the top 5 layout and design patterns you should follow.",
        author: "uxGenie",
        date: "March 29, 2025",
        category: "UI/UX",
        tags: "UI Design, CSS, Frontend",
        image: "../assets/ui-design.jpg",
        bookmarks: 34,
        shares: 16,
        saves: 25,
        upvotes: 77,
        downvotes: 4,
        views: 850,
        comments: 4
    },
    {
        title: "Deploying Your Website for Free Using GitHub Pages",
        description: "This post explains how to deploy static websites for free using GitHub Pages.",
        author: "hostBuddy",
        date: "March 30, 2025",
        category: "Hosting",
        tags: "GitHub Pages, Deployment, Hosting",
        image: "../assets/githubpages.png",
        bookmarks: 18,
        shares: 9,
        saves: 12,
        upvotes: 48,
        downvotes: 2,
        views: 540,
        comments: 1
    },
    {
        title: "MySQL Joins Explained Visually",
        description: "Visual guide and examples of INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN in MySQL.",
        author: "dataDude",
        date: "April 2, 2025",
        category: "Database",
        tags: "MySQL, Joins, SQL",
        image: "../assets/sqljoins.png",
        bookmarks: 41,
        shares: 22,
        saves: 17,
        upvotes: 66,
        downvotes: 3,
        views: 780,
        comments: 3
    },
    {
        title: "Responsive Design: Mobile First Approach",
        description: "A deep dive into mobile-first development and how to make your site truly responsive.",
        author: "cssGuru",
        date: "April 6, 2025",
        category: "Responsive",
        tags: "Mobile First, CSS, Responsive Design",
        image: "../assets/mobile-first.jpg",
        bookmarks: 39,
        shares: 19,
        saves: 20,
        upvotes: 73,
        downvotes: 5,
        views: 910,
        comments: 6
    },
    {
        title: "Top 5 Chrome DevTools Tips You Didn't Know",
        description: "Hidden gems inside Chrome DevTools that can supercharge your debugging process.",
        author: "debugNinja",
        date: "April 5, 2025",
        category: "Debugging",
        tags: "Chrome DevTools, Debugging, Tricks",
        image: "../assets/devtools.png",
        bookmarks: 50,
        shares: 28,
        saves: 32,
        upvotes: 85,
        downvotes: 4,
        views: 1020,
        comments: 7
    }
];

postsData.forEach(post => {
    addPostToDisplay(post);
});
