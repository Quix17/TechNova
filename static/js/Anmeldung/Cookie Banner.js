document.addEventListener("DOMContentLoaded", function() {
    // Überprüfen, ob der Benutzer bereits zugestimmt hat
    const cookiesAccepted = localStorage.getItem("cookiesAccepted");

    if (cookiesAccepted !== "true") {
        // Wenn noch nicht zugestimmt, den Banner anzeigen
        document.getElementById("cookie-banner").style.display = "block";
    }

    // Beim Klick auf den "OK"-Button wird die Zustimmung gespeichert und der Banner ausgeblendet
    document.getElementById("accept-cookies").addEventListener("click", function() {
        // Zustimmung im LocalStorage speichern, wenn der Benutzer auf "OK" klickt
        localStorage.setItem("cookiesAccepted", "true"); // Zustimmung speichern
        document.getElementById("cookie-banner").style.display = "none"; // Banner ausblenden

        // Speichern der Zustimmung im Backend, nachdem der Benutzer auf OK geklickt hat
        const userId = localStorage.getItem('user_id');  // Sicherstellen, dass user_id vorhanden ist
        if (userId) {
            fetch('http://localhost:5000/save-cookies-acceptance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId: userId,  // Übernehme die userId
                    cookiesAccepted: true,  // Zustimmung ist 'true'
                }),
            })
            .then(response => response.json())
            .then(data => {
                // Erfolg nach Speicherung der Zustimmung in der DB
            })
            .catch(error => {
                // Fehlerbehandlung für die Speicherung
            });
        }
    });
});