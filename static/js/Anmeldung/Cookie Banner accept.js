// Funktion, um die user_id aus dem URL-Pfad zu extrahieren und im localStorage zu speichern
function storeUserIdFromPath() {
    const path = window.location.pathname;
    const match = path.match(/\/dashboard_id(\d+)/); // Wir suchen nach 'dashboard_id' gefolgt von einer Zahl

    if (match) {
        const userId = match[1];  // Extrahierte user_id
        localStorage.setItem('user_id', userId);  // Speichern der user_id im localStorage
        console.log("User ID gespeichert:", userId);
    } else {
        console.log("Keine User ID im URL-Pfad gefunden.");
    }
}

// Funktion beim Laden der Seite ausführen
window.onload = function() {
    storeUserIdFromPath();  // User ID aus dem URL-Pfad extrahieren und speichern

    const cookiesAccepted = localStorage.getItem('cookiesAccepted'); // true oder false als String
    const userId = localStorage.getItem('user_id'); // user_id aus dem localStorage holen

    // Prüfen, ob die User ID im localStorage vorhanden ist und wir den Zustand des Cookies prüfen müssen
    if (userId) {
        console.log("Überprüfe, ob die Zustimmung bereits in der Datenbank gespeichert wurde...");

        fetch('http://localhost:5000/check-cookies-acceptance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                userId: userId,  // Die userId aus dem localStorage
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.cookiesAccepted === null) {
                // Wenn in der DB noch keine Zustimmung gespeichert ist, senden wir sie
                console.log('Keine Zustimmung in der DB gefunden, sende Anfrage zur Speicherung...');

                fetch('http://localhost:5000/save-cookies-acceptance', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        userId: userId,  // Die tatsächliche userId aus dem localStorage
                        cookiesAccepted: true,  // Wir setzen es auf 'true', weil der Benutzer zugestimmt hat
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message === 'Zustimmung erfolgreich gespeichert') {
                        // Nach erfolgreichem Senden der Zustimmung, speichern wir sie im localStorage
                        localStorage.setItem('cookiesAccepted', 'true');
                        console.log('Zustimmung wurde in der DB und im localStorage gespeichert!');
                    }
                })
                .catch(error => {
                    console.error('Fehler beim Senden der Zustimmung:', error);
                });
            } else {
                // Wenn die Zustimmung bereits in der DB gespeichert wurde, setzen wir den localStorage-Wert auf 'true'
                localStorage.setItem('cookiesAccepted', 'true');
                console.log('Zustimmung wurde bereits in der DB gespeichert.');
            }
        })
        .catch(error => {
            console.error('Fehler beim Abrufen der Zustimmung aus der DB:', error);
        });
    } else {
        console.log('Keine User ID gefunden!');
    }
};