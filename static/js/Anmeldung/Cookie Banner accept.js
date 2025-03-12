window.addEventListener("DOMContentLoaded", function() {
    // Funktion, um die user_id aus dem URL-Pfad zu extrahieren und im localStorage zu speichern
    function storeUserIdFromPath() {
        const path = window.location.pathname;

        // RegEx, um die User ID nach '/dashboard_id' zu extrahieren
        const match = path.match(/\/dashboard_id(\d+)/);

        if (match) {
            const userId = match[1];  // Extrahierte user_id
            localStorage.setItem('user_id', userId);  // Speichern der user_id im localStorage
        }
    }

    // Sicherstellen, dass der Wert erst nach dem Laden der Seite überprüft wird
    storeUserIdFromPath();  // User ID aus dem URL-Pfad extrahieren und speichern

    // Hole die cookiesAccepted und userId einmal aus dem localStorage
    const cookiesAccepted = localStorage.getItem('cookiesAccepted');
    const userId = localStorage.getItem('user_id'); // user_id aus dem localStorage holen

    // Wenn der Benutzer eingeloggt ist und eine User ID vorhanden ist
    if (userId && cookiesAccepted === 'true') {
        // Nur dann an die DB senden, wenn die Zustimmung vorliegt
        fetch('http://localhost:5000/save-cookies-acceptance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                userId: userId,
                cookiesAccepted: true,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Zustimmung erfolgreich gespeichert') {
                // Hier könnte der Banner ausgeblendet oder andere Aktionen erfolgen
            }
        })
        .catch(error => {
            // Keine sensiblen Daten im Fehler-Log
            console.error('Fehler beim Senden der Zustimmung:', error);
        });
    }
});