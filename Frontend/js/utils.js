const toggleBtn = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const closeBtn = document.getElementById('close-menu');

toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation(); 
    mobileMenu.classList.remove('translate-x-full');
    mobileMenu.classList.add('translate-x-0');
});

closeBtn.addEventListener('click', () => {
    mobileMenu.classList.remove('translate-x-0');
    mobileMenu.classList.add('translate-x-full');
});

document.addEventListener('click', (e) => {
    if (!mobileMenu.contains(e.target) && !toggleBtn.contains(e.target)) {
        mobileMenu.classList.remove('translate-x-0');
        mobileMenu.classList.add('translate-x-full');
    }
});

document.querySelectorAll(".logout").forEach((click) => {
    click.addEventListener("click", () => {
        const confirmed = confirm("Are you sure you want to logout?");
        if (confirmed) {
            window.location.href = "./index.html";
        }
    });
});
