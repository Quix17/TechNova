document.addEventListener("DOMContentLoaded", function() {
    const bugItems = document.querySelectorAll('.bug-item');

    // Funktion, um die Bugs nacheinander erscheinen zu lassen
    function animateBugs() {
        bugItems.forEach((item, index) => {
            // Verzögerung für jedes Element, damit sie nacheinander erscheinen
            setTimeout(() => {
                item.style.transition = "opacity 0.6s ease, transform 0.6s ease"; // Übergangseffekte
                item.style.opacity = 1;  // Sichtbar machen
                item.style.transform = "translateY(0)";  // Hochbewegen
            }, index * 500); // Verzögerung von 500ms zwischen den Bugs
        });
    }

    // Hover-Effekt für das Verschieben nach rechts
    bugItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = "translateX(10px)";  // Verschiebt nach rechts
        });

        item.addEventListener('mouseleave', () => {
            item.style.transform = "translateX(0)";  // Setzt die Position zurück
        });
    });

    // Starte die Animation
    animateBugs();
});