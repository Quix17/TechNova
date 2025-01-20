// Funktion, die den Blur-Effekt auf andere Karten anwendet
function addBlurEffect(exceptCard) {
    // Alle Karten auswählen
    const cards = document.querySelectorAll('.card');

    // Jede Karte prüfen
    cards.forEach(card => {
        if (card !== exceptCard) {
            // Blur-Effekt auf alle Karten anwenden, außer der hoverte Karte
            card.style.filter = 'blur(5px)';
        }
    });
}

// Funktion, die den Blur-Effekt entfernt
function removeBlurEffect() {
    // Alle Karten zurücksetzen, indem der Filter entfernt wird
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.filter = 'none';
    });
}

// Hinzufügen der Event-Listener für die Hover-Effekte
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', () => addBlurEffect(card));
        card.addEventListener('mouseleave', removeBlurEffect);
    });
});