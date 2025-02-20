document.addEventListener("DOMContentLoaded", function() {
    // Direkt nach dem Laden der Seite wird überprüft, ob der Nutzer zugestimmt hat
    if (!localStorage.getItem("cookiesAccepted")) {
        // Wenn noch nicht zugestimmt, den Banner anzeigen
        document.getElementById("cookie-banner").style.display = "block";
    }

    // Beim Klick auf den "OK"-Button wird die Zustimmung gespeichert und der Banner ausgeblendet
    document.getElementById("accept-cookies").addEventListener("click", function() {
        localStorage.setItem("cookiesAccepted", "true"); // Zustimmung speichern
        document.getElementById("cookie-banner").style.display = "none"; // Banner ausblenden
    });
});
