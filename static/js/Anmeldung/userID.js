// Funktion, um die user_id aus der URL zu extrahieren und im localStorage zu speichern
function storeUserId() {
    // Überprüfen, ob die user_id in der URL vorhanden ist
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('userID'); // user_id aus der URL holen

    if (userId) {
        // Speichern der user_id im localStorage
        localStorage.setItem('user_id', userId);
        console.log("User ID gespeichert:", userId);  // Ausgabe zur Bestätigung
    } else {
        console.log("Keine User ID in der URL gefunden.");
    }
}

// Funktion beim Laden der Seite ausführen
window.onload = storeUserId;