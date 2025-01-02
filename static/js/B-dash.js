document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll('.card'); // Alle Karten
    let currentHoveredCard = null; // Variable für die aktuell gehovte Karte

    cards.forEach((card, index) => {
        card.addEventListener('mouseover', () => {
            // Den Blur auf alle anderen Karten anwenden, wenn die aktuelle Karte gehovt wird
            cards.forEach((otherCard, otherIndex) => {
                if (otherIndex !== index) {
                    otherCard.style.filter = 'blur(5px)'; // Setzt den Blur auf andere Karten
                }
            });
        });

        card.addEventListener('mouseout', () => {
            // Entfernt den Blur von allen Karten, wenn der Hover-Effekt endet
            cards.forEach((otherCard) => {
                otherCard.style.filter = ''; // Entfernt den Blur
            });
        });
    });
});