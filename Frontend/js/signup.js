const form = document.querySelector("form");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }
    if (/\s/.test(password)) {
        alert("Password should not contain spaces!");
        return;
    }
    if (password.length < 8) {
        alert("Password must be at least 8 characters long!");
        return;
    }
    try {
        await submitSignupData({ username, email, password });
    } catch (error) {
        console.error("Error:", error);
    }
});


async function submitSignupData(data) {
    try {
        const response = await fetch("http://localhost:8000/user/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        alert(result.message || result.detail);
        if (result.message) {
            window.location.href = "./login.html";
        }
    } catch (error) {
        throw error;
    }
}
