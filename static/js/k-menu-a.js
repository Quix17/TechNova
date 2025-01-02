// JavaScript für interaktive Funktionen

// Funktion, um Benachrichtigungen zu speichern
function toggleNotifications() {
    const emailNotifications = document.getElementById("email-notifications").checked;
    const smsNotifications = document.getElementById("sms-notifications").checked;

    // Hier kann man dann eine API-Aufruf oder Speicherung implementieren
    console.log(`E-Mail Benachrichtigungen: ${emailNotifications ? "Aktiviert" : "Deaktiviert"}`);
    console.log(`SMS Benachrichtigungen: ${smsNotifications ? "Aktiviert" : "Deaktiviert"}`);

    alert("Einstellungen wurden gespeichert!");
}

// Funktion zur Bestätigung des Konto-Löschens
function confirmDeleteAccount() {
    const confirmation = confirm("Bist du sicher, dass du dein Konto löschen möchtest? Dieser Vorgang kann nicht rückgängig gemacht werden.");

    if (confirmation) {
        // Hier kann man dann den tatsächlichen Löschvorgang auslösen
        console.log("Konto wird gelöscht...");
        alert("Dein Konto wurde gelöscht.");
    } else {
        console.log("Konto löschen abgebrochen.");
        alert("Konto löschen abgebrochen.");
    }
}