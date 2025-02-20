// Funktion, um die user_id aus dem URL-Pfad zu extrahieren und im localStorage zu speichern
function storeUserIdFromPath() {
    // Holen des Pfades der URL (z.B. '/dashboard_id2')
    const path = window.location.pathname;

    // Verwende eine Regular Expression, um die user_id aus dem URL-Pfad zu extrahieren
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

    const cookiesAccepted = localStorage.getItem('cookiesAccepted') === 'true'; // true oder false
    console.log('cookiesAccepted aus localStorage:', cookiesAccepted);

    const userId = localStorage.getItem('user_id'); // user_id aus dem localStorage holen

    if (cookiesAccepted !== null && userId) {
        fetch('http://localhost:5000/save-cookies-acceptance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                userId: userId,  // Hier wird die tatsächliche userId aus dem localStorage verwendet
                cookiesAccepted: cookiesAccepted,
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Antwort vom Server:', data);
            })
            .catch(error => {
                console.error('Fehler beim Senden der Zustimmung:', error);
            });
    } else {
        console.log('Kein Wert für cookiesAccepted oder userId im localStorage gefunden.');
    }
};