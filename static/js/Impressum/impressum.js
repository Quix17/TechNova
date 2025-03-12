document.addEventListener("DOMContentLoaded", () => {
    const infoItems = document.querySelectorAll(".info-item");
    const headerText = document.querySelector("h1");

    // Funktion für Scroll-Effekte (Einzelnes Einblenden mit Delay)
    const fadeInOnScroll = () => {
        infoItems.forEach((item, index) => {
            const rect = item.getBoundingClientRect();
            if (rect.top < window.innerHeight - 50) {
                setTimeout(() => {
                    item.classList.add("visible");
                }, index * 150); // Verzögerung von 150ms pro Element
            }
        });
    };

    fadeInOnScroll(); // Initial check
    window.addEventListener("scroll", fadeInOnScroll);

    // Header Schriftanimation
    headerText.style.opacity = 0;
    setTimeout(() => {
        headerText.style.transition = "opacity 1s ease-in-out";
        headerText.style.opacity = 1;
    }, 500);
});