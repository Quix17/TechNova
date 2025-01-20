document.addEventListener("DOMContentLoaded", function() {
    const infoItems = document.querySelectorAll('.info-item');

    // Setzt alle Info-Items initial auf transparent
    infoItems.forEach(item => {
        item.style.opacity = 0;
        item.style.transform = 'translateY(20px)';
    });

    // Animiert die einzelnen Info-Items beim Laden der Seite
    infoItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = 1;
            item.style.transform = 'translateY(0)';
            item.style.transition = 'all 0.5s ease-out';
        }, index * 200); // Verzögerung zwischen den Elementen
    });
});