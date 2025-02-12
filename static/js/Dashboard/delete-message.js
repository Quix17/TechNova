   // Zeige das Modal an, wenn der Benutzer den "Konto löschen"-Button klickt
   document.getElementById('delete-account-btn').addEventListener('click', function() {
    document.getElementById('delete-warning-modal').style.display = 'block'; // Modal sichtbar machen
});

// Schließe das Modal
function closeModal() {
    document.getElementById('delete-warning-modal').style.display = 'none'; // Modal verstecken
}

// Bestätige die Löschung und sende das Formular ab
function confirmDeletion() {
    // Formular absenden, wenn der Benutzer die Löschung bestätigt
    document.getElementById('delete-account-form').submit();
}