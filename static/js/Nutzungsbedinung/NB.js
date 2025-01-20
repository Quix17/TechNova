// Dynamisches Anzeigen von Abschnittsinhalten
document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".section-title");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const content = this.nextElementSibling;
            content.classList.toggle("show");
        });
    });

    // Smooth Scroll für die Navigation
    const navLinks = document.querySelectorAll('.main-header .header-content a');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            window.scrollTo({
                top: targetElement.offsetTop - 90, // Headerhöhe berücksichtigen
                behavior: 'smooth'
            });
        });
    });
});
