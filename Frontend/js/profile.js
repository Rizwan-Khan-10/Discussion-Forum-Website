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