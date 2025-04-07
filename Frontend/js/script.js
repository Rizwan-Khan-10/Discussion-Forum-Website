window.addEventListener("DOMContentLoaded", () => {
    const scrollToHash = (hash) => {
        const el = document.querySelector(hash);
        if (el) {
            el.scrollIntoView({ behavior: "smooth" });
            setTimeout(() => {
                history.replaceState(null, null, window.location.pathname);
            }, 500); 
        }
    };

    const hash = window.location.hash;
    if (["#contact", "#forum", "#about", "#features"].includes(hash)) {
        scrollToHash(hash);
    }

    sessionStorage.removeItem("userId");
    sessionStorage.removeItem("username");
});
