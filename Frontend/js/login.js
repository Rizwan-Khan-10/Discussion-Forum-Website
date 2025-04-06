const form = document.querySelector("form");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        alert("Please enter both username and password!");
        return;
    }

    try {
        await loginUser({ email, password });
    } catch (error) {
        console.error("Error:", error);
    }
});

async function loginUser(data) {
    try {
        const response = await fetch("http://localhost:8000/user/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        alert(result.message || result.detail);
    } catch (error) {
        console.error("Fetch error:", error);
        alert("Something went wrong while logging in.");
    }
}
